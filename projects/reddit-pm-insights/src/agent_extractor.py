"""Extract "actually built" tools from Reddit posts using Claude API.

Uses Claude to classify each post and extract structured tool/workflow data,
filtering for real implementations vs. discussion threads.
"""

import os
from typing import Optional
import anthropic
import pandas as pd


class BuiltToolsExtractor:
    """Extract real, shipped tools from Reddit posts using Claude API."""

    EXTRACTION_PROMPT = """Analyze this Reddit post about PM tools/workflows.

POST:
Title: {title}
Body: {body}

TASK: Determine if this is a REAL BUILT TOOL (someone sharing an implementation)
or just discussion/opinion.

Respond with ONLY valid JSON (no markdown, no explanation):
{{
  "is_built_tool": boolean,
  "reject_reason": "string or null (if is_built_tool=false, why rejected)",
  "what_was_built": "one sentence, concrete (e.g. 'Slack bot that summarizes standup notes')",
  "stack": "named tools/languages used, comma-separated (e.g. 'Python, Claude API, Slack SDK')",
  "repo_link": "github/replit/streamlit/vercel link or null if not found",
  "demo_link": "live demo URL or null",
  "build_effort": "weekend project | ongoing tool | one-off script | unknown",
  "replicable_in_week": true,
  "replicability_reason": "brief note on why buildable (or not) by a TPM with Python/SQL"
}}

FILTERING RULES (reject if ALL of these fail):
- Post does NOT contain: "I built", "I made", "I automated", "I shipped", "here's how"
- Post does NOT contain: github.com, replit.com, streamlit.app, vercel.app link
- Post does NOT describe a concrete workflow with named tools

Only return is_built_tool=true if post has credible implementation evidence.
"""

    def __init__(self) -> None:
        """Initialize Claude API client."""
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def extract_post(self, title: str, body: str) -> Optional[dict]:
        """Extract structured data from a Reddit post using Claude.

        Args:
            title: Post title
            body: Post body text (first 500 chars)

        Returns:
            Parsed JSON dict or None if API fails
        """
        try:
            prompt = self.EXTRACTION_PROMPT.format(title=title, body=body[:500])

            message = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text.strip()

            # Parse JSON response
            import json
            result = json.loads(response_text)
            return result

        except Exception as e:
            print(f"  ⚠️  Extraction failed: {str(e)}")
            return None

    @staticmethod
    def process_dataframe(df: pd.DataFrame, max_posts: int = 100) -> pd.DataFrame:
        """Process dataframe of Reddit posts through extraction agent.

        Args:
            df: DataFrame with 'title' and 'selftext' columns
            max_posts: Max posts to extract (API cost limit)

        Returns:
            DataFrame of extracted, validated tools
        """
        extractor = BuiltToolsExtractor()
        results = []

        print(f"\n🔍 Extracting 'actually built' tools from {len(df)} posts...")
        print(f"   (processing up to {max_posts} for Claude extraction)\n")

        for idx, row in df.head(max_posts).iterrows():
            print(f"  [{idx+1}/{min(len(df), max_posts)}] {row['title'][:60]}...")

            extraction = extractor.extract_post(row['title'], row['selftext'])

            if extraction and extraction.get('is_built_tool'):
                results.append({
                    "what_was_built": extraction.get('what_was_built'),
                    "stack": extraction.get('stack'),
                    "repo_link": extraction.get('repo_link'),
                    "demo_link": extraction.get('demo_link'),
                    "build_effort": extraction.get('build_effort'),
                    "replicable_in_week": extraction.get('replicable_in_week'),
                    "replicability_reason": extraction.get('replicability_reason'),
                    "source_title": row['title'],
                    "source_url": row['url'],
                    "engagement": row['engagement_score'],
                    "subreddit": row['subreddit']
                })
                print(f"    ✅ Accepted: {extraction['what_was_built'][:50]}...")
            else:
                reason = extraction.get('reject_reason') if extraction else "Parse error"
                print(f"    ❌ Rejected: {reason}")

        # Convert to dataframe and sort
        results_df = pd.DataFrame(results)

        if results_df.empty:
            print("\n⚠️  No 'actually built' tools found in posts.")
            return results_df

        # Sort: replicable first, then by engagement
        results_df = results_df.sort_values(
            by=['replicable_in_week', 'engagement'],
            ascending=[False, False]
        )

        return results_df

    @staticmethod
    def save_markdown_table(df: pd.DataFrame, output_file: str) -> None:
        """Export results as markdown table.

        Args:
            df: Results dataframe
            output_file: Output markdown file path
        """
        if df.empty:
            content = "# Built Tools from Reddit PM Communities\n\nNo tools found matching criteria.\n"
        else:
            # Create markdown table
            rows = [
                "| What Was Built | Stack | Repo/Demo | Effort | Replicable? | Why? |",
                "|---|---|---|---|---|---|"
            ]

            for _, row in df.iterrows():
                # Format links
                repo_str = ""
                if row['repo_link']:
                    repo_str += f"[Repo]({row['repo_link']}) "
                if row['demo_link']:
                    repo_str += f"[Demo]({row['demo_link']})"
                repo_str = repo_str.strip() or "—"

                # Replicable yes/no with color
                replicable = "✅ Yes" if row['replicable_in_week'] else "⚠️ Maybe"

                rows.append(
                    f"| {row['what_was_built'][:40]}... | {row['stack'][:30]}... | {repo_str} | "
                    f"{row['build_effort']} | {replicable} | {row['replicability_reason'][:40]}... |"
                )

            content = f"""# PM-Built AI Tools & Workflows

Extracted from Reddit r/ProductManagement, r/ProductManagers, r/AIProductManagement.
**Filtered to: actual shipped implementations, not opinions.**

## Summary
- **Total tools found:** {len(df)}
- **Replicable by TPM in <1 week:** {df['replicable_in_week'].sum()}
- **Has public repo/demo:** {(df['repo_link'].notna() | df['demo_link'].notna()).sum()}

## Tools

{chr(10).join(rows)}

---

### Legend
- **Build Effort:** weekend project | ongoing tool | one-off script
- **Replicable?:** Could a TPM with Python/SQL rebuild in <1 week?
- **Engagement:** Reddit score + weighted comments

### Sources
"""

            for subreddit in df['subreddit'].unique():
                count = len(df[df['subreddit'] == subreddit])
                content += f"\n- r/{subreddit}: {count} tool(s)"

        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w') as f:
            f.write(content)

        print(f"\n📄 Markdown table saved to {output_file}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Run extraction on existing CSV
        csv_file = sys.argv[1]
        df = pd.read_csv(csv_file)
        results = BuiltToolsExtractor.process_dataframe(df, max_posts=50)

        if not results.empty:
            md_file = csv_file.replace('.csv', '_tools.md')
            BuiltToolsExtractor.save_markdown_table(results, md_file)
            print(f"\n✅ Extraction complete! Found {len(results)} built tools.")
        else:
            print("\n❌ No tools found.")
