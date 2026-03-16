## ADDED Requirements

### Requirement: uv project initialization
The project SHALL be initialized with `uv init` producing a valid `pyproject.toml` following PEP 621.

#### Scenario: Fresh project setup
- **WHEN** a developer clones the repository and runs `uv sync`
- **THEN** uv creates a `.venv/` virtual environment and installs all dependencies

### Requirement: Python version pinning
The project SHALL include a `.python-version` file specifying Python 3.12.

#### Scenario: Consistent Python version
- **WHEN** a developer runs `uv sync`
- **THEN** uv uses the Python version specified in `.python-version`

### Requirement: Core dependencies declared
The `pyproject.toml` SHALL declare `fastapi`, `uvicorn[standard]`, and `pydantic-settings` as runtime dependencies.

#### Scenario: Production dependencies available
- **WHEN** the virtual environment is synced
- **THEN** `fastapi`, `uvicorn`, and `pydantic-settings` are importable

### Requirement: Dev dependencies declared
The `pyproject.toml` SHALL declare `ruff` and `pytest` as development dependencies under a `[dependency-groups]` dev group.

#### Scenario: Dev tools available
- **WHEN** a developer runs `uv sync`
- **THEN** `ruff` and `pytest` are available in the virtual environment

### Requirement: Ruff configuration
The `pyproject.toml` SHALL include a `[tool.ruff]` section with line-length 88 and Python 3.12 target.

#### Scenario: Linting works out of the box
- **WHEN** a developer runs `uv run ruff check app/`
- **THEN** ruff lints the code with the configured rules
