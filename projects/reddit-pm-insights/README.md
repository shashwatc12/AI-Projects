# Reddit PM Insights Scraper

Scrapes top posts from Product Management subreddits, identifies "actually built" AI tools & workflows (not just opinions), and extracts replicable PM implementations using Claude API.

**Goal:** Find real shipped tools that PMs have built, not discussion threads or trend takes.

## Pipeline

### Step 1: Scrape Reddit (PRAW)
- Top posts from r/ProductManagement, r/ProductManagers, r/AIProductManagement (past month)
- Filter for AI/automation keywords (agent, automation, LLM, tool, etc.)
- Score by engagement (upvotes + 0.3× comments)

### Step 2: Theme Analysis
- Cluster posts into themes: AI Integration, Automation, Strategy, User Research, Analytics, Team/Process
- Show theme distribution and top posts per theme

### Step 3: Extract "Actually Built" Tools (Claude API)
- **Filter ruthlessly:** only keep posts with:
  - "I built" / "I made" / "I automated" in text, OR
  - GitHub/Replit/Streamlit/Vercel link, OR
  - Concrete workflow with named tools
- **Reject:** pure opinion/discussion posts, polls, career questions
- **Extract via Claude:** what was built, stack used, repo link, build effort, replicability
- **Sort:** replicable-in-a-week first, then by engagement
- **Output:** markdown table ranked by buildability

## Quick Start

### 1. Get API Credentials

**Reddit API** (free, 2 min):
- Go to https://reddit.com/prefs/apps
- Create app → Select "script" type
- Note your **client_id** and **client_secret**

**Claude API** (for tool extraction):
- Get key from https://console.anthropic.com
- Enables AI-powered classification of "actually built" vs. opinion posts

### 2. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with credentials
cp .env.example .env
# Edit .env and add:
# REDDIT_CLIENT_ID=...
# REDDIT_CLIENT_SECRET=...
# ANTHROPIC_API_KEY=...
```

### 3. Run Pipeline

```bash
# Full pipeline: scrape + theme analysis + tool extraction
python main.py

# Skip Claude extraction (theme analysis only)
python main.py --skip-extraction

# Extract tools from existing CSV (e.g., from previous run)
python main.py --extract-from data/reddit_pm_insights.csv

# Custom subreddits
python main.py --subreddits SideProject AIProductManagement

# Custom output
python main.py --output research/pm_tools.csv
```

## Output

### 1. Theme Analysis CSV
`data/reddit_pm_insights.csv` — all posts ranked by engagement:
```
title | subreddit | url | score | comments | engagement_score | created_utc
---
"I built a Slack bot that summarizes standups using GPT-4" | ProductManagement | https://reddit.com/... | 245 | 67 | 265.1 | 2024-09-06...
```

### 2. Theme Analysis Console Output
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
   1. "I automated roadmap reviews with Claude API..."
      Score: 523 | ProductManagement
```

### 3. Built Tools Markdown (AI-Extracted)
`data/reddit_pm_insights_built_tools.md` — actionable PM tools:
```
| What Was Built | Stack | Repo/Demo | Effort | Replicable? | Why? |
|---|---|---|---|---|---|
| Slack bot: standup summarization → JIRA | Python, Claude API, Slack SDK | [Repo](github.com/...) [Demo](streamlit.app/...) | weekend project | ✅ Yes | Clear stack, standard libs, no complex infra |
| BigQuery semantic layer UI | Python, Streamlit, BigQuery API | [Repo](github.com/...) | ongoing tool | ✅ Yes | Common PM data problem |
| ...
```

**Top-ranked first** = buildable by a TPM with Python/SQL in <1 week.

### 4. Built Tools CSV
`data/reddit_pm_insights_built_tools.csv` — structured for further analysis

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
