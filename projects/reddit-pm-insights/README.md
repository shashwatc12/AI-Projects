# Reddit PM Insights Scraper

Scrapes top posts from Product Management subreddits, filters for AI/automation themes, scores by engagement, and clusters results into actionable insights.

## What It Does

1. **Scrapes** top posts from r/ProductManagement, r/ProductManagers, r/AIProductManagement (past month)
2. **Filters** for AI/automation keywords (agent, automation, LLM, tool, etc.)
3. **Scores** posts by engagement (upvotes + weighted comments)
4. **Analyzes** themes and clusters posts (AI Integration, Automation, Strategy, etc.)
5. **Outputs** ranked CSV with title, link, score, theme

## Quick Start

### 1. Get Reddit API Credentials (2 min)

- Go to https://reddit.com/prefs/apps
- Click "Create app" → Select "script" type
- Note your **client_id** and **client_secret**

### 2. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with credentials
cp .env.example .env
# Edit .env and add your Reddit API credentials
```

### 3. Run Scraper

```bash
# Full pipeline (scrape + analyze)
python main.py

# Custom subreddits
python main.py --subreddits ArtificialIntelligence OpenAI

# Save to specific file
python main.py --output custom_output.csv
```

## Output

**CSV file** (`data/reddit_pm_insights.csv`):
```
title | subreddit | url | score | comments | engagement_score | created_utc
---
"How to implement AI agents in your product..." | ProductManagement | https://reddit.com/... | 245 | 67 | 265.1 | 2024-09-06...
```

**Console output** - Theme analysis:
```
THEME ANALYSIS SUMMARY
========================
Total Posts: 42
Unique Themes: 6

Theme Distribution:
  AI Integration .................... 18 (42.9%)
  Automation ........................ 12 (28.6%)
  Product Strategy ................. 8 (19.0%)
  ...

Top Posts by Theme:
📌 AI Integration
   1. "Deploying Claude API in production..."
      Score: 523 | ProductManagement
```

## Project Structure

```
reddit-pm-insights/
├── src/
│   ├── scraper.py      # Reddit API scraping
│   └── analyzer.py     # Theme clustering
├── main.py             # Entry point
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
├── README.md           # This file
└── data/               # Output CSV files
```

## Keywords Filtered

AI/automation focused: `ai, agent, automation, gpt, llm, claude, tool, algorithm, embedding, prompt, autonomous, reasoning`

## Troubleshooting

**"Invalid credentials"**
- Double-check Reddit client_id and client_secret in .env
- Ensure .env is in project root

**"No posts found"**
- Try different subreddits (use `--subreddits`)
- Increase time range (modify `time_filter` in scraper.py)
- Check if keywords need updating

**"praw not found"**
- Run: `pip install -r requirements.txt`

## Learning Value

This is a clean, scoped project (~45 min execution) covering:
- API integration (PRAW)
- Data filtering and scoring
- NLP-lite keyword matching
- Theme clustering
- CSV output and structured data

Great rep for vibe-coding interviews!
