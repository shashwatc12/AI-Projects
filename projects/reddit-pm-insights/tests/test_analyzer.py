"""Unit tests for analyzer module."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from analyzer import ThemeAnalyzer


class TestThemeAnalyzer:
    """Test suite for ThemeAnalyzer."""

    def test_themes_defined(self):
        """Test that themes are properly defined."""
        assert len(ThemeAnalyzer.THEMES) > 0
        assert "AI Integration" in ThemeAnalyzer.THEMES
        assert "Automation" in ThemeAnalyzer.THEMES

    def test_categorize_ai_integration(self):
        """Test categorization of AI integration post."""
        title = "Implementing Claude API in production"
        text = "We successfully integrated LLM models for feature suggestions."

        themes = ThemeAnalyzer.categorize_post(title, text)

        assert "AI Integration" in themes

    def test_categorize_automation(self):
        """Test categorization of automation post."""
        title = "Automating team workflows"
        text = "Using agents to automate roadmap updates and reviews."

        themes = ThemeAnalyzer.categorize_post(title, text)

        assert "Automation" in themes

    def test_categorize_multiple_themes(self):
        """Test post can match multiple themes."""
        title = "Using AI to automate user research"
        text = "Implementing automated surveys with LLM analysis for feedback."

        themes = ThemeAnalyzer.categorize_post(title, text)

        assert len(themes) > 1
        assert "AI Integration" in themes or "Automation" in themes

    def test_categorize_no_match(self):
        """Test post with no matching theme defaults to 'Other'."""
        title = "Random post about nothing"
        text = "This has no relevant keywords whatsoever."

        themes = ThemeAnalyzer.categorize_post(title, text)

        assert "Other" in themes

    def test_analyze_dataframe(self, sample_posts_dataframe):
        """Test full dataframe analysis."""
        analysis = ThemeAnalyzer.analyze_dataframe(sample_posts_dataframe)

        assert "theme_distribution" in analysis
        assert "theme_posts" in analysis
        assert "total_posts" in analysis
        assert "unique_themes" in analysis

        assert analysis["total_posts"] == 3
        assert analysis["unique_themes"] > 0

    def test_theme_distribution_sorted(self, sample_posts_dataframe):
        """Test that theme distribution is sorted by count."""
        analysis = ThemeAnalyzer.analyze_dataframe(sample_posts_dataframe)

        counts = list(analysis["theme_distribution"].values())

        # Verify descending order
        assert counts == sorted(counts, reverse=True)

    def test_theme_posts_mapping(self, sample_posts_dataframe):
        """Test that posts are correctly mapped to themes."""
        analysis = ThemeAnalyzer.analyze_dataframe(sample_posts_dataframe)

        # Verify structure of theme_posts
        for theme, posts in analysis["theme_posts"].items():
            assert isinstance(posts, list)
            for post in posts:
                assert "title" in post
                assert "url" in post
                assert "score" in post
                assert "subreddit" in post
