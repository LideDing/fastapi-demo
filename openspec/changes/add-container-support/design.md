## Context

The FastAPI application uses `uv` for dependency management and Python 3.13. It requires several environment variables for OIDC authentication (`OIDC_*`) and app configuration (`APP_*`). The app starts via `uvicorn app.main:app`.

## Goals / Non-Goals

**Goals:**
- Multi-stage Dockerfile: build with `uv` to install dependencies, slim runtime image
- `run.sh` script that builds and runs with `podman run`, passing all required env vars
- Production-ready defaults (non-root user, proper signal handling)

**Non-Goals:**
- Docker Compose / pod orchestration
- CI/CD pipeline configuration
- Health check probes in container (app already has `/health`)

## Decisions

### 1. Base image: `python:3.13-slim`

**Choice**: Use official `python:3.13-slim` as the runtime base. Use a build stage with `uv` for dependency installation.

**Rationale**: Slim image keeps size small (~150MB). Multi-stage avoids shipping `uv` and build tools in the final image.

### 2. Dependency installation: `uv` in build stage

**Choice**: Install `uv` via `pip` in the build stage, run `uv sync --no-dev` to create the virtualenv, then copy only the `.venv` to the runtime stage.

**Rationale**: Consistent with the project's existing `uv`-based workflow. `--no-dev` excludes test/lint tools.

### 3. Run script: `run.sh` with `podman run`

**Choice**: A bash script that builds the image with `podman build` and runs it with `podman run`, reading env vars from an `.env` file or command-line defaults.

**Rationale**: Simple, single-command workflow. Using `--env-file .env` keeps secrets out of the command line.

### 4. Non-root user in container

**Choice**: Create an `appuser` in the Dockerfile and run the process as that user.

**Rationale**: Security best practice. Avoids running as root inside the container.

## Risks / Trade-offs

- **[No .env file]** → Script will fail if `.env` doesn't exist. Mitigation: script checks for `.env` and prints a helpful message.
- **[Image size]** → `python:3.13-slim` is ~150MB. Mitigation: acceptable for this use case; alpine would be smaller but has musl compatibility issues.
