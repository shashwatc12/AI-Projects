#!/usr/bin/env python3
"""Main entry point for Reddit PM insights scraper."""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from scraper import RedditPMScraper
from analyzer import ThemeAnalyzer
import pandas as pd


def main() -> None:
    """Run the scraping and analysis pipeline."""
    parser = argparse.ArgumentParser(
        description="Scrape Reddit PM insights and cluster by themes"
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
        help="Subreddits to scrape (default: ProductManagement ProductManagers AIProductManagement)"
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Run theme analysis after scraping"
    )

    args = parser.parse_args()

    try:
        # Step 1: Scrape Reddit
        print("🔄 Starting Reddit scraping...\n")
        scraper = RedditPMScraper()
        df_results = scraper.run(
            output_file=args.output,
            subreddits=args.subreddits
        )

        if df_results.empty:
            print("⚠️  No results found. Check your API credentials or try different subreddits.")
            return

        # Step 2: Analyze themes (optional)
        if args.analyze or True:  # Always analyze by default
            print("\n🔍 Analyzing themes...\n")
            analysis = ThemeAnalyzer.analyze_dataframe(df_results)
            ThemeAnalyzer.print_summary(analysis)

        print(f"\n✅ Complete! Results saved to {args.output}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check .env file has REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET")
        print("2. Verify Reddit API credentials are correct")
        print("3. Ensure praw is installed: pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()
