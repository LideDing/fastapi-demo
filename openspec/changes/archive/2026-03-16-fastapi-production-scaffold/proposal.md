## Why

This is a greenfield project that needs a well-structured FastAPI application scaffold before any business logic can be developed. A production-grade foundation with clear separation of routing and business logic will accelerate all future development and enforce consistent patterns from the start.

## What Changes

- Initialize a `pyproject.toml` managed by **uv** with FastAPI and core production dependencies
- Create a layered project structure: routers (HTTP layer) separated from services (business logic)
- Set up application entry point with lifespan management, CORS, and structured logging
- Configure development tooling: virtual environment via uv, linting (ruff), formatting, and a dev server command
- Add a health-check endpoint as the first working route to validate the scaffold
- Provide configuration management via environment variables (pydantic-settings)

## Capabilities

### New Capabilities
- `project-setup`: uv project initialization, pyproject.toml, virtual environment, and dependency management
- `app-scaffold`: FastAPI application factory, lifespan events, middleware stack, and structured configuration
- `router-service-pattern`: Router/service separation pattern with a health-check reference implementation

### Modified Capabilities
<!-- None — this is a new project -->

## Impact

- **New files**: Full project directory structure under `app/`, `pyproject.toml`, `.python-version`
- **Dependencies**: fastapi, uvicorn, pydantic-settings, ruff (dev)
- **Tooling**: Requires `uv` to be installed on the developer machine
