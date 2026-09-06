"""Shared test fixtures and configuration."""

import pytest
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_posts_dataframe():
    """Fixture: Sample posts dataframe for testing."""
    return pd.DataFrame({
        "title": [
            "How to implement AI agents in your product",
            "Best user research practices",
            "Automating PM workflows with tools"
        ],
        "subreddit": ["ProductManagement", "ProductManagers", "ProductManagement"],
        "url": ["http://example.com/1", "http://example.com/2", "http://example.com/3"],
        "score": [250, 150, 200],
        "comments": [45, 30, 40],
        "engagement_score": [263.5, 159.0, 212.0],
        "selftext": [
            "Integrating GPT models for feature suggestions",
            "Conducting interviews to understand pain points",
            "Using automation to manage roadmap updates"
        ],
        "created_utc": ["2024-09-01", "2024-09-02", "2024-09-03"]
    })


@pytest.fixture
def empty_dataframe():
    """Fixture: Empty dataframe."""
    return pd.DataFrame()
