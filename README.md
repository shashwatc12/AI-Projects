# AI Projects

A monorepo for AI/ML applications, intelligent backend systems, and data analytics solutions built with Python, SQL, and Claude AI integration.

## Quick Start

```bash
# Setup
git clone https://github.com/shashwatc12/ai-projects.git
cd ai-projects

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Navigate to a project
cd projects/<project-name>
pip install -r requirements.txt

# Run tests
pytest tests/

# Run linting & formatting
black .
flake8 .
```

## Project Structure

- **`/projects/`** - Individual AI/ML and data projects (each self-contained)
- **`/shared/`** - Shared utilities, database schemas, and configurations
- **`/docs/`** - Architecture documentation and API references
- **`/scripts/`** - Utility scripts for deployment and data migration

## Technology Stack

- **Python 3.11+** - Primary language
- **pytest** - Testing framework
- **Claude API** - AI integration (when applicable)
- **SQL** - Data queries and ETL
- **black/flake8/mypy** - Code quality tools

## Development Guidelines

See [CLAUDE.md](./CLAUDE.md) for:
- Detailed development commands
- Project structure conventions
- Python and SQL standards
- Git workflow

## License

Apache 2.0
