## ADDED Requirements

### Requirement: Application factory
The application SHALL provide a `create_app()` function in `app/main.py` that returns a configured `FastAPI` instance.

#### Scenario: App creation
- **WHEN** `create_app()` is called
- **THEN** it returns a FastAPI instance with title, version, and all routers included

### Requirement: Lifespan management
The application SHALL use FastAPI's lifespan context manager for startup/shutdown events.

#### Scenario: Startup logging
- **WHEN** the application starts
- **THEN** a log message indicating successful startup is emitted

#### Scenario: Shutdown logging
- **WHEN** the application shuts down
- **THEN** a log message indicating graceful shutdown is emitted

### Requirement: CORS middleware
The application SHALL include CORS middleware configured from settings.

#### Scenario: CORS headers present
- **WHEN** a cross-origin request is made to any endpoint
- **THEN** the response includes appropriate CORS headers based on configured allowed origins

### Requirement: Structured configuration
The application SHALL load configuration from environment variables using a `Settings` class in `app/config.py` built on `pydantic-settings`.

#### Scenario: Default configuration
- **WHEN** no environment variables are set
- **THEN** the application starts with sensible defaults (debug=false, host=0.0.0.0, port=8000)

#### Scenario: Environment override
- **WHEN** `APP_DEBUG=true` is set as an environment variable
- **THEN** the Settings instance reflects `debug=True`

### Requirement: Uvicorn entry point
The `app/main.py` SHALL include an `if __name__ == "__main__"` block that starts uvicorn with settings from configuration.

#### Scenario: Direct execution
- **WHEN** a developer runs `uv run python -m app.main`
- **THEN** uvicorn starts serving the application on the configured host and port
