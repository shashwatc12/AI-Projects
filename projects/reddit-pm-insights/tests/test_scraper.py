"""Unit tests for scraper module."""

import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scraper import RedditPMScraper


class TestRedditPMScraper:
    """Test suite for RedditPMScraper."""

    def test_ai_keywords_exist(self):
        """Test that AI keywords are defined."""
        assert len(RedditPMScraper.AI_KEYWORDS) > 0
        assert "ai" in RedditPMScraper.AI_KEYWORDS
        assert "agent" in RedditPMScraper.AI_KEYWORDS

    def test_initialization(self):
        """Test scraper initialization."""
        with patch("praw.Reddit"):
            scraper = RedditPMScraper()
            assert scraper.posts_data == []

    def test_filter_empty_dataframe(self):
        """Test filtering with empty data."""
        with patch("praw.Reddit"):
            scraper = RedditPMScraper()
            df = scraper.filter_ai_keywords()
            assert df.empty

    def test_score_calculation(self):
        """Test engagement score calculation."""
        import pandas as pd

        with patch("praw.Reddit"):
            scraper = RedditPMScraper()

            # Create test data
            test_data = pd.DataFrame({
                "score": [100, 50],
                "comments": [10, 20],
                "title": ["AI Post", "PM Post"],
                "subreddit": ["PM", "PM"],
                "url": ["http://example.com", "http://example.com"],
                "created_utc": ["2024-01-01", "2024-01-01"]
            })

            scored = scraper.score_posts(test_data)

            # First post: 100 + (10 * 0.3) = 103
            assert scored.iloc[0]["engagement_score"] == 103.0

            # Second post: 50 + (20 * 0.3) = 56
            assert scored.iloc[1]["engagement_score"] == 56.0

    def test_keyword_filtering(self):
        """Test keyword filtering logic."""
        import pandas as pd

        with patch("praw.Reddit"):
            scraper = RedditPMScraper()

            # Create test data with mixed AI/non-AI content
            test_data = [
                {
                    "title": "Using Claude AI in product development",
                    "subreddit": "PM",
                    "url": "http://example.com",
                    "score": 100,
                    "comments": 20,
                    "created_utc": "2024-01-01",
                    "selftext": "Great insights about LLM integration"
                },
                {
                    "title": "Best practices for user research",
                    "subreddit": "PM",
                    "url": "http://example.com",
                    "score": 50,
                    "comments": 10,
                    "created_utc": "2024-01-01",
                    "selftext": "Interviewing users to understand their needs"
                }
            ]

            scraper.posts_data = test_data
            filtered = scraper.filter_ai_keywords()

            # Only first post should have AI keywords
            assert len(filtered) == 1
            assert "Claude" in filtered.iloc[0]["title"]
