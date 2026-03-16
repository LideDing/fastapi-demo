## 1. Project Initialization

- [x] 1.1 Run `uv init` to create `pyproject.toml` with project metadata (name, version, python-requires)
- [x] 1.2 Add `.python-version` file pinning Python 3.13 (matched system Python)
- [x] 1.3 Add runtime dependencies: `fastapi`, `uvicorn[standard]`, `pydantic-settings`
- [x] 1.4 Add dev dependencies: `ruff`, `pytest`, `httpx` (for test client)
- [x] 1.5 Configure `[tool.ruff]` in pyproject.toml (line-length=88, target=py313)
- [x] 1.6 Run `uv sync` to create `.venv/` and install all dependencies

## 2. Application Configuration

- [x] 2.1 Create `app/__init__.py`
- [x] 2.2 Create `app/config.py` with `Settings` class using pydantic-settings (debug, host, port, cors_origins)

## 3. Application Factory

- [x] 3.1 Create `app/main.py` with `create_app()` function, lifespan context manager, and CORS middleware
- [x] 3.2 Add `if __name__ == "__main__"` uvicorn entry point in `app/main.py`

## 4. Router-Service Pattern (Health Check)

- [x] 4.1 Create `app/models/__init__.py` and `app/models/health.py` with `HealthResponse` model
- [x] 4.2 Create `app/services/__init__.py` and `app/services/health.py` with `check_health()` function
- [x] 4.3 Create `app/routers/__init__.py` and `app/routers/health.py` with `GET /health` endpoint
- [x] 4.4 Register health router in `create_app()`

## 5. Verification

- [x] 5.1 Run `uv run ruff check app/` and fix any lint issues
- [x] 5.2 Start the dev server with `uv run python -m app.main` and verify `GET /health` returns `{"status": "ok"}`
