"""Analyze and cluster Reddit PM posts into themes."""

from typing import Dict, List
import pandas as pd
from collections import defaultdict


class ThemeAnalyzer:
    """Cluster posts into product management themes."""

    THEMES = {
        "AI Integration": {
            "keywords": ["integrate", "implement", "llm", "gpt", "ai", "tool"],
            "description": "Using AI to enhance product features"
        },
        "Product Strategy": {
            "keywords": ["strategy", "roadmap", "vision", "goal", "market"],
            "description": "Strategic planning and market positioning"
        },
        "Automation": {
            "keywords": ["automate", "automation", "workflow", "agent", "autonomous"],
            "description": "Automating tasks and processes"
        },
        "User Research": {
            "keywords": ["user", "research", "feedback", "pain point", "behavior"],
            "description": "Understanding user needs and behaviors"
        },
        "Analytics & Data": {
            "keywords": ["analytics", "data", "metric", "tracking", "measure"],
            "description": "Data-driven decision making"
        },
        "Team & Process": {
            "keywords": ["team", "process", "agile", "sprint", "execution"],
            "description": "Team organization and execution"
        },
    }

    @staticmethod
    def categorize_post(title: str, text: str) -> List[str]:
        """Categorize post into themes based on keywords.

        Args:
            title: Post title
            text: Post body text

        Returns:
            List of matching theme names
        """
        combined_text = (title + " " + text).lower()
        themes = []

        for theme_name, theme_data in ThemeAnalyzer.THEMES.items():
            if any(kw in combined_text for kw in theme_data["keywords"]):
                themes.append(theme_name)

        return themes if themes else ["Other"]

    @staticmethod
    def analyze_dataframe(df: pd.DataFrame) -> Dict[str, any]:
        """Analyze DataFrame and cluster into themes.

        Args:
            df: DataFrame with title and selftext columns

        Returns:
            Dictionary with theme analysis
        """
        theme_counts = defaultdict(int)
        theme_posts = defaultdict(list)

        for _, row in df.iterrows():
            themes = ThemeAnalyzer.categorize_post(
                row["title"],
                row["selftext"]
            )

            for theme in themes:
                theme_counts[theme] += 1
                theme_posts[theme].append({
                    "title": row["title"],
                    "url": row["url"],
                    "score": row["engagement_score"],
                    "subreddit": row["subreddit"]
                })

        return {
            "theme_distribution": dict(sorted(
                theme_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )),
            "theme_posts": dict(theme_posts),
            "total_posts": len(df),
            "unique_themes": len(theme_counts)
        }

    @staticmethod
    def print_summary(analysis: Dict) -> None:
        """Print human-readable theme analysis.

        Args:
            analysis: Analysis dictionary from analyze_dataframe
        """
        print("\n" + "="*60)
        print("THEME ANALYSIS SUMMARY")
        print("="*60)

        print(f"\nTotal Posts Analyzed: {analysis['total_posts']}")
        print(f"Unique Themes Found: {analysis['unique_themes']}\n")

        print("Theme Distribution:")
        print("-" * 40)
        for theme, count in analysis["theme_distribution"].items():
            pct = (count / analysis["total_posts"]) * 100
            print(f"  {theme:.<30} {count:>3} ({pct:>5.1f}%)")

        print("\n" + "="*60)
        print("Top Posts by Theme (Highest Engagement):")
        print("="*60)

        for theme, posts in analysis["theme_posts"].items():
            sorted_posts = sorted(posts, key=lambda x: x["score"], reverse=True)
            print(f"\n📌 {theme}")
            for i, post in enumerate(sorted_posts[:3], 1):
                print(f"   {i}. {post['title'][:60]}...")
                print(f"      Score: {post['score']:.0f} | {post['subreddit']}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        df = pd.read_csv(sys.argv[1])
        analysis = ThemeAnalyzer.analyze_dataframe(df)
        ThemeAnalyzer.print_summary(analysis)
