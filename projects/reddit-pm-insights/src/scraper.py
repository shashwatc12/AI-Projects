"""Reddit Product Management insights scraper.

Pulls top posts from PM subreddits, filters for AI/automation themes,
scores by engagement, and outputs structured results.
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

import pandas as pd
import praw
from dotenv import load_dotenv


class RedditPMScraper:
    """Scrape and analyze PM-related Reddit posts."""

    # Keywords to filter for AI PM OS + AI SDLC innovation
    AI_KEYWORDS = {
        # AI/LLM tech
        "ai", "agent", "automation", "gpt", "llm", "claude", "openai",
        "embedding", "langchain", "reasoning", "prompt", "autonomous",

        # PM OS + workflows
        "workflow", "automation", "specification", "spec generation",
        "roadmap", "backlog", "planning", "sync", "status update",
        "decision support", "data-driven", "jira", "linear", "asana",

        # SDLC innovation
        "sdlc", "development workflow", "engineering", "ci/cd", "release",
        "code review", "testing", "test generation", "documentation",

        # Process evolution
        "scrum alternative", "kanban alternative", "agile", "lean",
        "evidence-driven", "outcome-focused", "iterative",

        # Quick-win signals
        "built", "tool", "script", "automation", "saved time",
        "productivity", "efficiency", "integration"
    }

    def __init__(self) -> None:
        """Initialize Reddit API connection."""
        load_dotenv()

        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "pm-ai-scraper/1.0"),
        )
        self.posts_data: List[Dict[str, Any]] = []

    def fetch_posts(
        self,
        subreddits: List[str],
        time_filter: str = "month",
        limit: int = 100,
    ) -> None:
        """Fetch top posts from specified subreddits.

        Args:
            subreddits: List of subreddit names (without r/)
            time_filter: Time period filter (week, month, year, all)
            limit: Number of posts per subreddit
        """
        for subreddit_name in subreddits:
            print(f"Fetching from r/{subreddit_name}...")
            subreddit = self.reddit.subreddit(subreddit_name)

            for post in subreddit.top(time_filter=time_filter, limit=limit):
                # Skip stickied posts and ads
                if post.stickied or post.is_self is False:
                    continue

                self.posts_data.append({
                    "title": post.title,
                    "subreddit": subreddit_name,
                    "url": f"https://reddit.com{post.permalink}",
                    "score": post.score,
                    "comments": post.num_comments,
                    "created_utc": datetime.fromtimestamp(post.created_utc),
                    "selftext": post.selftext[:200],  # First 200 chars
                })

    def filter_ai_keywords(self) -> pd.DataFrame:
        """Filter posts containing AI/automation keywords."""
        if not self.posts_data:
            return pd.DataFrame()

        df = pd.DataFrame(self.posts_data)

        # Convert title and text to lowercase for matching
        df["text_combined"] = (
            (df["title"] + " " + df["selftext"]).str.lower()
        )

        # Check if any keyword is in the combined text
        df["has_ai_keyword"] = df["text_combined"].apply(
            lambda x: any(keyword in x for keyword in self.AI_KEYWORDS)
        )

        return df[df["has_ai_keyword"]].copy()

    def score_posts(self, df: pd.DataFrame) -> pd.DataFrame:
        """Score posts by engagement (upvotes + weighted comments).

        Args:
            df: DataFrame of posts

        Returns:
            DataFrame sorted by engagement score
        """
        # Normalize scores (comments weighted at 0.3x upvotes)
        df["engagement_score"] = df["score"] + (df["comments"] * 0.3)

        # Sort by engagement
        df = df.sort_values("engagement_score", ascending=False)

        return df[["title", "subreddit", "url", "score", "comments",
                    "engagement_score", "created_utc"]].reset_index(drop=True)

    def run(
        self,
        output_file: str = "data/reddit_pm_insights.csv",
        subreddits: List[str] | None = None,
    ) -> pd.DataFrame:
        """Run full scraping pipeline.

        Args:
            output_file: Path to save CSV results
            subreddits: List of subreddits to scrape

        Returns:
            DataFrame of scored posts
        """
        if subreddits is None:
            subreddits = [
                "ProductManagement",
                "ProductManagers",
                "AIProductManagement",
            ]

        print(f"Starting scrape from {len(subreddits)} subreddits...")
        self.fetch_posts(subreddits, time_filter="month", limit=100)

        print(f"Filtering for AI/automation keywords...")
        df_filtered = self.filter_ai_keywords()

        if df_filtered.empty:
            print("No posts found matching criteria.")
            return df_filtered

        print(f"Found {len(df_filtered)} matching posts. Scoring...")
        df_scored = self.score_posts(df_filtered)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save to CSV
        df_scored.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")

        return df_scored


if __name__ == "__main__":
    scraper = RedditPMScraper()
    results = scraper.run()
    print(f"\nTop insights:")
    print(results.head(10))
