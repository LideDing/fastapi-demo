## ADDED Requirements

### Requirement: Dockerfile builds a runnable image
The project SHALL include a `Dockerfile` that produces a container image capable of running the FastAPI application.

#### Scenario: Successful image build
- **WHEN** `podman build -t fastapi-demo .` is run from the project root
- **THEN** the build SHALL complete successfully producing a tagged image

#### Scenario: Container starts and serves traffic
- **WHEN** the container is started with all required environment variables
- **THEN** the application SHALL listen on port 8000 and respond to `/health` with HTTP 200

### Requirement: Run script for podman
The project SHALL include a `run.sh` script that builds the image and starts a container using `podman run`.

#### Scenario: Run script with .env file
- **WHEN** `./run.sh` is executed and a `.env` file exists with all required variables
- **THEN** the script SHALL build the image and start the container with env vars loaded from `.env`

#### Scenario: Run script without .env file
- **WHEN** `./run.sh` is executed and no `.env` file exists
- **THEN** the script SHALL print an error message explaining how to create the `.env` file and exit

### Requirement: .dockerignore excludes unnecessary files
The project SHALL include a `.dockerignore` file that excludes `.venv`, `.git`, `__pycache__`, tests, and other non-runtime files.

#### Scenario: Build context is minimal
- **WHEN** the Docker image is built
- **THEN** the build context SHALL NOT include `.venv/`, `.git/`, `__pycache__/`, `tests/`, or `openspec/` directories
