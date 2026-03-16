# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Production-ready FastAPI application with router/service separation pattern.

## Architecture

```
app/
  main.py          # create_app() factory, lifespan, CORS middleware
  config.py        # pydantic-settings Settings class (env prefix: APP_)
  routers/         # HTTP route definitions only — no business logic
  services/        # Business logic functions called by routers
  models/          # Pydantic request/response schemas
```

Pattern: routers delegate to services; each feature domain has matching files in routers/, services/, and models/.

## Commands

- `uv sync` — install/update all dependencies into `.venv/`
- `uv run python -m app.main` — start dev server (host/port from APP_HOST/APP_PORT env vars)
- `uv run ruff check app/` — lint
- `uv run ruff format app/` — format
- `uv run pytest` — run tests

## Tooling

- **Dependencies**: managed by `uv` via `pyproject.toml`
- **Linting/formatting**: ruff (configured in pyproject.toml)
- **Config**: environment variables with `APP_` prefix (e.g., `APP_DEBUG=true`)
- **Workflow**: OpenSpec (`openspec` CLI) for spec-driven changes
