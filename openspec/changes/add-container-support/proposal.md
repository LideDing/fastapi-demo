## Why

The application needs to be containerized for consistent deployment. A Dockerfile and a convenience script using `podman run` will allow quick local testing and production deployment.

## What Changes

- Add a multi-stage `Dockerfile` using `uv` for dependency installation and Python 3.13 as the runtime base
- Add a `run.sh` script that builds the image and runs the container with `podman`, passing OIDC and app environment variables
- Add a `.dockerignore` to keep the image lean

## Capabilities

### New Capabilities
- `container-deploy`: Dockerfile and podman run script for building and running the application in a container

### Modified Capabilities

_(none)_

## Impact

- **Files**: New `Dockerfile`, `run.sh`, `.dockerignore` at project root
- **Dependencies**: No new Python dependencies; requires `podman` on the host
- **Deployment**: Enables containerized deployment via a single `./run.sh` command
