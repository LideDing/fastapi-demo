## 1. Dockerfile

- [x] 1.1 Create multi-stage `Dockerfile` with `uv` build stage and `python:3.13-slim` runtime stage, non-root user, exposing port 8000

## 2. Docker Ignore

- [x] 2.1 Create `.dockerignore` excluding `.venv/`, `.git/`, `__pycache__/`, `tests/`, `openspec/`, `*.pyc`, `.env`

## 3. Run Script

- [x] 3.1 Create `run.sh` that checks for `.env` file, builds image with `podman build`, and runs container with `podman run --env-file .env`
- [x] 3.2 Make `run.sh` executable

## 4. Environment Template

- [x] 4.1 Create `.env.example` with all required environment variables documented
