# Travel Research Agent

A Google ADK-based agent that researches travel destinations using Google Search and web scraping sub-agents, powered by Gemini models and served via FastAPI.

## Tech Stack

- Python + Google ADK
- Google Gemini models (LLM)
- FastAPI (serving)
- Google Search tool + web scraping agents for gathering destination info

## Project Structure

Follows the adk-samples repo convention:

```
travel-research/
  travel_research/       # Main package
    __init__.py
    agent.py             # Root agent definition
    ...                  # Sub-agents, tools, prompts
  tests/                 # pytest tests
  eval/                  # ADK eval test sets
  pyproject.toml
  requirements.txt
  env.example
  README.md
```

## Commands

- **Install deps:** `pip install -r requirements.txt`
- **Run agent:** `python -m travel_research` or via ADK CLI
- **Run tests:** `pytest tests/`
- **Run evals:** Use ADK eval framework in `eval/`

## Environment Variables

Required (never commit these):

- `GOOGLE_API_KEY` — Gemini API key
- `GOOGLE_CLOUD_PROJECT` — GCP project ID

Copy `env.example` to `.env` and fill in values.

## Code Style

- PEP 8 basics
- No strict type hints or docstrings required
- Keep it simple and readable

## Architecture Guidelines

- Create sub-agents for distinct tasks wherever possible
- Root agent orchestrates, sub-agents do the work
- Use Google Search tool for discovery, sub-agents for extracting info from found sites

## Workflow Rules

- Always run tests before committing
- Ask before creating new files
- Keep changes minimal — don't refactor or add features beyond what's requested
- Use sub-agents (Task tool) for parallel independent work

## Testing

- pytest for unit and integration tests
- ADK eval framework for agent quality evaluation
- Tests must pass before any commit
