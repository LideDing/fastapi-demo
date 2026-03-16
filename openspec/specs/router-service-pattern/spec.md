## ADDED Requirements

### Requirement: Router-service separation
Each feature domain SHALL have a router module in `app/routers/` that defines HTTP endpoints and a corresponding service module in `app/services/` that contains business logic. Routers SHALL NOT contain business logic directly.

#### Scenario: Router delegates to service
- **WHEN** an HTTP request hits a router endpoint
- **THEN** the router calls the corresponding service function and returns its result

### Requirement: Health check router
The application SHALL include a health-check router at `app/routers/health.py` that exposes a `GET /health` endpoint.

#### Scenario: Health check success
- **WHEN** a GET request is made to `/health`
- **THEN** the response status is 200 and the body is `{"status": "ok"}`

### Requirement: Health check service
The health-check business logic SHALL reside in `app/services/health.py`, returning structured health status data.

#### Scenario: Service returns health data
- **WHEN** the health service `check_health()` function is called
- **THEN** it returns a dict with key `"status"` set to `"ok"`

### Requirement: Response models
Each router SHALL define Pydantic response models in `app/models/` for type-safe API responses.

#### Scenario: Health response model
- **WHEN** the health endpoint returns a response
- **THEN** the response is validated against a `HealthResponse` model in `app/models/health.py`

### Requirement: Router registration
All routers SHALL be registered in the application factory via `app.include_router()`.

#### Scenario: Router auto-included
- **WHEN** `create_app()` is called
- **THEN** the health router is included and `/health` is accessible
