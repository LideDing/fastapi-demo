## Context

This is a greenfield FastAPI project with no existing code. The repository currently contains only a LICENSE, .gitignore, and openspec configuration. We need to establish the foundational project structure that all future features will build upon.

The target developer workflow uses `uv` for dependency management and virtual environments, with `ruff` for linting/formatting.

## Goals / Non-Goals

**Goals:**
- Establish a clean, layered project structure (routers → services → models)
- Configure uv-managed dependencies with a locked virtual environment
- Provide a working health-check endpoint as a reference implementation
- Set up structured configuration via environment variables
- Include dev tooling (ruff, uvicorn reload mode)

**Non-Goals:**
- Database integration or ORM setup (future change)
- Authentication/authorization (future change)
- Docker/containerization (future change)
- CI/CD pipeline configuration
- Frontend or template rendering

## Decisions

### 1. Project layout: flat `app/` package

Use a single `app/` package at the repo root with sub-packages for each layer:

```
app/
  __init__.py
  main.py          # Application factory + lifespan
  config.py         # pydantic-settings based config
  routers/          # HTTP route definitions only
  services/         # Business logic functions
  models/           # Pydantic request/response schemas
```

**Rationale**: Flat layout is simpler than `src/` layout for applications (not libraries). Sub-packages enforce the router/service separation at the file-system level.

### 2. Dependency management: uv with pyproject.toml

Use `uv init` to create `pyproject.toml` and manage the virtual environment at `.venv/`.

**Rationale**: uv is fast, supports PEP 621 natively, and handles venv creation + dependency resolution in one tool. No need for pip, pip-tools, or poetry.

### 3. Application factory pattern

Use a `create_app()` function in `app/main.py` rather than a module-level `app` instance. This allows different configurations for testing vs production.

### 4. Configuration via pydantic-settings

Use `pydantic-settings` to load config from environment variables and `.env` files. A single `Settings` class in `app/config.py`.

**Rationale**: Type-safe, validates at startup, integrates naturally with FastAPI's dependency injection.

### 5. Linting/formatting: ruff only

Use `ruff` for both linting and formatting (replaces black + isort + flake8).

**Rationale**: Single tool, extremely fast, configured in `pyproject.toml`.

## Risks / Trade-offs

- **[Opinionated structure]** → The router/service split may feel heavy for trivial endpoints. Mitigation: the health-check demonstrates the pattern is lightweight.
- **[No database layer yet]** → Services will be pure functions initially. Mitigation: the layered structure makes adding a DB layer non-breaking.
- **[uv maturity]** → uv is newer than pip/poetry. Mitigation: uv has reached stable releases and is widely adopted; fallback to pip is trivial since we use standard pyproject.toml.
