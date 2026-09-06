"""Research agent for high-impact AI PM ideas aligned with user goals.

Searches Reddit for:
1. AI PM OS ideas (personal + team workflow automation)
2. SDLC innovation (moving beyond Scrum/Kanban)
3. Quick-win implementations (buildable in 1-2 weeks)
4. Reusable infrastructure patterns
"""

from typing import Optional, Dict, Any
import anthropic


class AIpmResearchAgent:
    """Research agent for discovering high-impact AI PM ideas."""

    RESEARCH_PROMPT = """You are researching high-impact AI PM ideas from Reddit discussions.
The user is building:
1. An AI PM OS (personal productivity + team collaboration + decision support + automation)
2. AI-native SDLC (learning from Anthropic's approach, moving away from Scrum/Kanban)

Looking for:
- Tools/workflows for AI-driven PM (spec generation, status sync, automation)
- Teams that moved away from traditional Scrum/Kanban
- Quick wins (1-2 week builds with immediate ROI)
- Reusable infrastructure/patterns

CONTEXT (Reddit posts):
{context}

TASK:
1. Identify the HIGHEST-IMPACT IDEAS that align with user's goals
2. For each idea:
   - What problem does it solve?
   - Why is it high-impact for PMs?
   - Could the user build it in 1-2 weeks?
   - What infrastructure/patterns could other PMs reuse?
   - How does it relate to Anthropic-style AI-native SDLC?

3. Synthesize: What are the 3-5 ACTIONABLE IDEAS the user should build first?
   - Quick wins that compound
   - Blocks for larger AI PM OS
   - Reusable patterns

Output as structured JSON:
{{
  "highest_impact_ideas": [
    {{
      "idea": "string (1-2 sentence pitch)",
      "problem": "what PM pain does it solve?",
      "build_time": "1-2 weeks | 2-4 weeks | ongoing",
      "quick_win": true/false,
      "replicable_pattern": "is this reusable by other PMs?",
      "anthropic_connection": "how does this relate to Anthropic's approach?",
      "source_posts": ["list of Reddit post titles that inspired this"]
    }}
  ],
  "synthesis": "2-3 paragraph narrative of: what's working, what's missing, what you should build",
  "priority_roadmap": [
    {{
      "order": 1,
      "idea": "idea title",
      "why_first": "reasoning",
      "blocks": ["what does this unblock?"]
    }}
  ],
  "infrastructure_opportunities": [
    "reusable SDK | template | pattern that other PMs would adopt"
  ]
}}
"""

    def __init__(self) -> None:
        """Initialize Claude API client."""
        self.client = anthropic.Anthropic()

    def synthesize_research(self, reddit_posts: list[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize research from Reddit posts into high-impact ideas.

        Args:
            reddit_posts: List of post dicts with title, selftext, engagement_score

        Returns:
            Structured research findings with ideas, synthesis, roadmap
        """
        # Build context from top posts
        context_items = []
        for post in reddit_posts[:20]:  # Top 20 by engagement
            context_items.append(
                f"- **{post['title']}** (engagement: {post['engagement_score']:.0f})\n"
                f"  {post['selftext'][:300]}...\n"
            )

        context = "\n".join(context_items)

        try:
            message = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": self.RESEARCH_PROMPT.format(context=context)
                    }
                ]
            )

            response_text = message.content[0].text.strip()

            # Parse JSON
            import json
            result = json.loads(response_text)
            return result

        except Exception as e:
            print(f"❌ Research synthesis failed: {str(e)}")
            return None

    @staticmethod
    def print_research_findings(findings: Dict[str, Any]) -> None:
        """Print research findings in human-readable format.

        Args:
            findings: Research synthesis from agent
        """
        if not findings:
            print("⚠️  No research findings available.")
            return

        print("\n" + "="*70)
        print("🔬 HIGH-IMPACT AI PM IDEAS RESEARCH")
        print("="*70)

        # Print synthesis
        if findings.get('synthesis'):
            print("\n📊 SYNTHESIS")
            print("-" * 70)
            print(findings['synthesis'])

        # Print ideas
        print("\n\n💡 HIGHEST-IMPACT IDEAS")
        print("-" * 70)
        for i, idea in enumerate(findings.get('highest_impact_ideas', []), 1):
            print(f"\n{i}. {idea['idea']}")
            print(f"   Problem: {idea['problem']}")
            print(f"   Build time: {idea['build_time']}")
            print(f"   Quick win? {idea['quick_win']}")
            print(f"   Replicable? {idea['replicable_pattern']}")
            print(f"   Anthropic connection: {idea['anthropic_connection']}")

        # Print priority roadmap
        print("\n\n🗺️  PRIORITY ROADMAP")
        print("-" * 70)
        for item in findings.get('priority_roadmap', []):
            print(f"\n{item['order']}. {item['idea']}")
            print(f"   Why first: {item['why_first']}")
            if item.get('blocks'):
                print(f"   Unblocks: {', '.join(item['blocks'])}")

        # Print infrastructure opportunities
        if findings.get('infrastructure_opportunities'):
            print("\n\n🏗️  REUSABLE INFRASTRUCTURE")
            print("-" * 70)
            for opp in findings['infrastructure_opportunities']:
                print(f"  • {opp}")

        print("\n" + "="*70)

    @staticmethod
    def save_research_memo(findings: Dict[str, Any], output_file: str) -> None:
        """Save research findings as markdown memo.

        Args:
            findings: Research synthesis
            output_file: Output markdown file path
        """
        import os
        import json

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        content = f"""# AI PM OS & SDLC Research Findings

Generated from Reddit PM communities analysis.
**Goal:** High-impact ideas for AI-native PM OS and SDLC innovation.

## Executive Summary

{findings.get('synthesis', 'No synthesis available')}

## Highest-Impact Ideas

"""
        for i, idea in enumerate(findings.get('highest_impact_ideas', []), 1):
            content += f"""
### {i}. {idea['idea']}

- **Problem:** {idea['problem']}
- **Build time:** {idea['build_time']}
- **Quick win?** {idea['quick_win']}
- **Replicable?** {idea['replicable_pattern']}
- **Anthropic connection:** {idea['anthropic_connection']}
- **Source posts:** {', '.join(idea.get('source_posts', []))}

"""

        content += "\n## Priority Roadmap\n\n"
        for item in findings.get('priority_roadmap', []):
            content += f"""
### {item['order']}. {item['idea']}

**Why first:** {item['why_first']}

"""
            if item.get('blocks'):
                content += f"**Unblocks:** {', '.join(item['blocks'])}\n\n"

        if findings.get('infrastructure_opportunities'):
            content += "\n## Reusable Infrastructure Opportunities\n\n"
            for opp in findings['infrastructure_opportunities']:
                content += f"- {opp}\n"

        content += f"\n---\n\n## Raw Findings (JSON)\n\n```json\n{json.dumps(findings, indent=2)}\n```\n"

        with open(output_file, 'w') as f:
            f.write(content)

        print(f"\n📄 Research memo saved to {output_file}")


if __name__ == "__main__":
    import pandas as pd
    import sys

    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        print(f"Loading research data from {csv_file}...")
        df = pd.read_csv(csv_file)

        # Convert to list of dicts
        posts = df.to_dict('records')

        # Run research agent
        print("\n🤖 Running research synthesis agent...\n")
        agent = AIpmResearchAgent()
        findings = agent.synthesize_research(posts)

        if findings:
            # Print to console
            AIpmResearchAgent.print_research_findings(findings)

            # Save memo
            memo_file = csv_file.replace('.csv', '_research_memo.md')
            AIpmResearchAgent.save_research_memo(findings, memo_file)

            print(f"\n✅ Research complete!")
        else:
            print("❌ Research synthesis failed.")
