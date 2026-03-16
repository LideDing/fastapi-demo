## ADDED Requirements

### Requirement: OIDC configuration
The system SHALL read OIDC provider settings from environment variables: `OIDC_ISSUER_URL` (required), `OIDC_CLIENT_ID` (required), `OIDC_CLIENT_SECRET` (required), `OIDC_REDIRECT_URL` (required), and `OIDC_SCOPES` (default `openid,profile`). The system SHALL also require `APP_SECRET_KEY` for session cookie signing.

#### Scenario: Valid OIDC configuration
- **WHEN** all required OIDC environment variables are set
- **THEN** the application SHALL start successfully

#### Scenario: Missing required OIDC configuration
- **WHEN** any required OIDC environment variable is not set
- **THEN** the application SHALL fail to start with a validation error

### Requirement: OIDC login route
The system SHALL provide a `GET /oidc/login` route that redirects the user to the TAI Auth Center authorization page. The route SHALL accept an optional `next` query parameter to remember the original URL.

#### Scenario: Login redirect
- **WHEN** a user accesses `GET /oidc/login?next=/hello`
- **THEN** the system SHALL save `/hello` in the session and redirect (302) to the TAI authorization endpoint with `client_id`, `redirect_uri`, `scope`, and `state` parameters

### Requirement: OIDC callback route
The system SHALL provide a `GET /oidc/callback` route that handles the authorization code exchange. It SHALL exchange the authorization code for tokens, fetch user info, store user info in the session, and redirect to the saved `next` URL.

#### Scenario: Successful callback
- **WHEN** the TAI Auth Center redirects to `/oidc/callback?code=AUTH_CODE&state=STATE`
- **THEN** the system SHALL exchange the code for tokens, fetch user info, store it in the session, and redirect (302) to the saved `next` URL (or `/` if none)

#### Scenario: Callback error
- **WHEN** the callback receives an `error` parameter or the code exchange fails
- **THEN** the system SHALL respond with HTTP 401 and an error message

### Requirement: OIDC logout route
The system SHALL provide a `GET /oidc/logout` route that clears the user session and redirects to the root path.

#### Scenario: Logout
- **WHEN** a user accesses `GET /oidc/logout`
- **THEN** the system SHALL clear the session and redirect (302) to `/`

### Requirement: Session-based authentication dependency
The system SHALL provide a `require_auth` FastAPI dependency that checks for a valid user session. If the user is not logged in, it SHALL redirect to the login page with the current URL as the `next` parameter.

#### Scenario: Authenticated user
- **WHEN** a request has a valid session with user info
- **THEN** the dependency SHALL return the user info and allow the request

#### Scenario: Unauthenticated user
- **WHEN** a request has no session or an expired session
- **THEN** the dependency SHALL redirect (302) to `/oidc/login?next=<current_url>`

### Requirement: Health endpoint remains public
The `/health` endpoint SHALL NOT require authentication.

#### Scenario: Health check without session
- **WHEN** a GET request is made to `/health` without a session
- **THEN** the system SHALL respond with HTTP 200 and the health status

### Requirement: Hello endpoint requires authentication
The `/hello` endpoint SHALL require a valid user session via OIDC login.

#### Scenario: Authenticated hello request
- **WHEN** a GET request is made to `/hello` with a valid session
- **THEN** the system SHALL respond with HTTP 200 and the hello response

#### Scenario: Unauthenticated hello request
- **WHEN** a GET request is made to `/hello` without a valid session
- **THEN** the system SHALL redirect (302) to `/oidc/login?next=/hello`
