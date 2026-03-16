## ADDED Requirements

### Requirement: Database configuration
The system SHALL read database connection settings from environment variable `APP_DB_URL` (e.g., `postgresql+asyncpg://postgres:mysecretpassword@localhost:5433/fastapi_demo`). The system SHALL also require `APP_JWT_SECRET` for JWT signing and `APP_JWT_EXPIRE_MINUTES` (default: 60) for token lifetime.

#### Scenario: Valid database configuration
- **WHEN** `APP_DB_URL` and `APP_JWT_SECRET` are set
- **THEN** the application SHALL start and establish a database connection pool successfully

#### Scenario: Missing database configuration
- **WHEN** `APP_DB_URL` or `APP_JWT_SECRET` is not set
- **THEN** the application SHALL fail to start with a validation error

### Requirement: User registration
The system SHALL provide a `POST /auth/register` endpoint that accepts `username`, `password`, and optional `email`. It SHALL hash the password using bcrypt and store the user in the `users` table. The `username` SHALL be unique.

#### Scenario: Successful registration
- **WHEN** `POST /auth/register` is called with a unique `username` and valid `password`
- **THEN** the system SHALL create the user, return HTTP 201 with `user_id` and `username`

#### Scenario: Duplicate username
- **WHEN** `POST /auth/register` is called with an already-existing `username`
- **THEN** the system SHALL return HTTP 409 with an error message

#### Scenario: Password too short
- **WHEN** `POST /auth/register` is called with a `password` shorter than 8 characters
- **THEN** the system SHALL return HTTP 422

### Requirement: Local password login
The system SHALL provide a `POST /auth/login` endpoint that accepts `username` and `password` (form data or JSON). It SHALL verify the bcrypt hash and, on success, return a signed JWT access token.

#### Scenario: Successful login
- **WHEN** `POST /auth/login` is called with correct `username` and `password`
- **THEN** the system SHALL return HTTP 200 with `{"access_token": "<jwt>", "token_type": "bearer"}`

#### Scenario: Wrong password
- **WHEN** `POST /auth/login` is called with an incorrect `password`
- **THEN** the system SHALL return HTTP 401 with detail `"Invalid credentials"`

#### Scenario: Unknown user
- **WHEN** `POST /auth/login` is called with a non-existent `username`
- **THEN** the system SHALL return HTTP 401 with detail `"Invalid credentials"`

### Requirement: JWT validation
The system SHALL validate Bearer JWT tokens in the `Authorization` header. The JWT payload SHALL contain `sub` (user_id as string) and `exp`. Expired or tampered tokens SHALL be rejected.

#### Scenario: Valid JWT
- **WHEN** a request includes `Authorization: Bearer <valid_jwt>`
- **THEN** the authentication dependency SHALL resolve to the corresponding user with their groups

#### Scenario: Expired JWT
- **WHEN** a request includes `Authorization: Bearer <expired_jwt>`
- **THEN** the system SHALL return HTTP 401 with detail `"Token expired"`

#### Scenario: Invalid JWT signature
- **WHEN** a request includes `Authorization: Bearer <tampered_jwt>`
- **THEN** the system SHALL return HTTP 401 with detail `"Invalid token"`

### Requirement: User data model
The system SHALL maintain a `users` table with columns: `id` (UUID PK), `username` (unique, not null), `email` (nullable), `hashed_password` (nullable, null for OIDC-only users), `external_id` (nullable, OIDC `sub`), `is_active` (boolean, default true), `created_at` (timestamp).

#### Scenario: OIDC user stored locally
- **WHEN** an OIDC login succeeds for the first time
- **THEN** the system SHALL upsert a user row with `external_id = sub` and `hashed_password = null`

#### Scenario: Local user has no external_id
- **WHEN** a user registers via `POST /auth/register`
- **THEN** `external_id` SHALL be null and `hashed_password` SHALL be set
