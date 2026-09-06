# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

**AI-Projects** is a monorepo for AI/ML applications, data analytics solutions, and intelligent backend systems. Projects here combine Python, SQL, and AI capabilities (including Claude API integration).

## Project Structure

```
/
├── projects/           # Individual project directories (each project is self-contained)
├── shared/            # Shared utilities, configs, database schemas
├── docs/              # Architecture and API documentation
└── scripts/           # Utility scripts (deployment, migration, etc.)
```

Each project under `/projects/` should have:
- `src/` - Source code
- `tests/` - Unit and integration tests
- `requirements.txt` - Python dependencies (or `pyproject.toml`)
- `README.md` - Project-specific documentation

## Development Commands

**Python & Dependencies**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies for a project
cd projects/<project-name>
pip install -r requirements.txt

# Run tests for a specific project
cd projects/<project-name>
pytest tests/

# Run with coverage
pytest tests/ --cov=src/
```

**Code Quality**
```bash
# Lint (flake8)
flake8 projects/<project-name>/src/

# Format (black)
black projects/<project-name>/

# Type checking (mypy)
mypy projects/<project-name>/src/
```

**Database & SQL**
```bash
# Run database migrations (project-dependent)
alembic upgrade head

# Interactive SQL development
psql -d <database-name> -f scripts/queries/<query-name>.sql
```

## Key Development Notes

**Token Efficiency:**
- When analyzing code, review file structure with `Glob` before deep dives
- For large projects, focus on critical paths and avoid redundant exploration
- Use `/skip` permission in recurring reviews to reduce prompts

**Python Standards:**
- Use `src/` layout for installable projects
- Type hints required in function signatures
- Pytest for testing (use `conftest.py` for fixtures)
- Virtual environments isolated per project

**SQL & Data:**
- Store schemas in `shared/schemas/` with version naming
- Use parameterized queries (no f-strings for SQL)
- Document complex queries with `-- Purpose:` comments

**AI Integration:**
- Claude API keys only in environment variables (`.env` in `.gitignore`)
- Use streaming for long-running AI calls
- Log API usage and costs per project

**Git Workflow:**
- Feature branches: `feature/<name>`
- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`
- Squash commits before merge

## Session Configuration

See `.claude/settings.json` for:
- Permission allowlists (reduces prompts)
- Environment variable setup
- Pre-approved bash commands
