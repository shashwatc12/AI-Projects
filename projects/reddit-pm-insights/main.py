#!/usr/bin/env python3
"""Main entry point for Reddit PM insights scraper.

Pipeline:
1. Scrape Reddit (PRAW)
2. Filter for AI/automation keywords
3. Theme analysis (clustering)
4. Extract "actually built" tools (Claude API)
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from scraper import RedditPMScraper
from analyzer import ThemeAnalyzer
from agent_extractor import BuiltToolsExtractor
from research_agent import AIpmResearchAgent
import pandas as pd


def main() -> None:
    """Run the full research pipeline."""
    parser = argparse.ArgumentParser(
        description="Scrape Reddit PM insights: themes + actually-built tools"
    )
    parser.add_argument(
        "--output",
        default="data/reddit_pm_insights.csv",
        help="Output CSV file path"
    )
    parser.add_argument(
        "--subreddits",
        nargs="+",
        default=["ProductManagement", "ProductManagers", "AIProductManagement"],
        help="Subreddits to scrape"
    )
    parser.add_argument(
        "--skip-extraction",
        action="store_true",
        help="Skip Claude-based tool extraction (default: run extraction)"
    )
    parser.add_argument(
        "--extract-from",
        help="Extract tools from existing CSV file (alternative to scraping)"
    )
    parser.add_argument(
        "--research",
        action="store_true",
        help="Run AI PM OS & SDLC research synthesis (requires ANTHROPIC_API_KEY)"
    )

    args = parser.parse_args()

    try:
        # STEP 1: Scrape Reddit (or load existing)
        if args.extract_from:
            print(f"📂 Loading existing CSV: {args.extract_from}\n")
            df_results = pd.read_csv(args.extract_from)
        else:
            print("🔄 Step 1: Scraping Reddit...\n")
            scraper = RedditPMScraper()
            df_results = scraper.run(
                output_file=args.output,
                subreddits=args.subreddits
            )

        if df_results.empty:
            print("⚠️  No results found. Check credentials or try different subreddits.")
            return

        # STEP 2: Theme Analysis
        print("\n🔍 Step 2: Theme analysis...\n")
        analysis = ThemeAnalyzer.analyze_dataframe(df_results)
        ThemeAnalyzer.print_summary(analysis)

        # STEP 3: Extract "Actually Built" Tools (Claude API)
        if not args.skip_extraction:
            print("\n🤖 Step 3: Extracting 'actually built' tools (Claude API)...\n")
            try:
                tools_df = BuiltToolsExtractor.process_dataframe(df_results, max_posts=50)

                if not tools_df.empty:
                    # Save markdown table
                    md_file = args.output.replace('.csv', '_built_tools.md')
                    BuiltToolsExtractor.save_markdown_table(tools_df, md_file)

                    # Also save as CSV
                    csv_file = args.output.replace('.csv', '_built_tools.csv')
                    tools_df.to_csv(csv_file, index=False)
                    print(f"   Saved CSV to {csv_file}")

                    print(f"\n✨ Found {len(tools_df)} replicable PM tools!")
                    print(f"   {tools_df['replicable_in_week'].sum()} are buildable in <1 week")
                else:
                    print("\n⚠️  No 'actually built' tools found (may need different subreddits)")
            except Exception as e:
                print(f"\n⚠️  Extraction skipped: {str(e)}")
                print("   (Ensure ANTHROPIC_API_KEY is set in .env)")
        else:
            print("\n⏭️  Skipping tool extraction (--skip-extraction)")

        # STEP 4: Research synthesis (AI PM OS + SDLC innovation)
        if args.research:
            print("\n🔬 Step 4: Synthesizing high-impact AI PM ideas...\n")
            try:
                research_agent = AIpmResearchAgent()
                findings = research_agent.synthesize_research(df_results.to_dict('records'))

                if findings:
                    # Print to console
                    AIpmResearchAgent.print_research_findings(findings)

                    # Save memo
                    memo_file = args.output.replace('.csv', '_research_memo.md')
                    AIpmResearchAgent.save_research_memo(findings, memo_file)
                else:
                    print("\n⚠️  Research synthesis failed.")
            except Exception as e:
                print(f"\n⚠️  Research skipped: {str(e)}")
                print("   (Ensure ANTHROPIC_API_KEY is set in .env)")
        else:
            print("\n⏭️  Skipping research synthesis (use --research flag)")

        print(f"\n✅ Research complete!")
        print(f"   📊 Theme analysis CSV: {args.output}")
        if not args.skip_extraction:
            print(f"   🛠️  Built tools markdown: {args.output.replace('.csv', '_built_tools.md')}")
        if args.research:
            print(f"   🔬 Research memo: {args.output.replace('.csv', '_research_memo.md')}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Reddit: Check .env has REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET")
        print("2. Claude: Check .env has ANTHROPIC_API_KEY")
        print("3. Install: pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()
