## MODIFIED Requirements

### Requirement: OIDC callback route
The system SHALL provide a `GET /auth/callback` route that handles the authorization code exchange. It SHALL exchange the authorization code for tokens, fetch user info, upsert the user into the local `users` table using `sub` as `external_id`, store the local `user_id` in the session, and redirect to the saved `next` URL.

#### Scenario: Successful callback — new OIDC user
- **WHEN** the OIDC provider redirects to `/auth/callback?code=AUTH_CODE&state=STATE` for a user not yet in the local database
- **THEN** the system SHALL create a new user row with `external_id=sub`, store `user_id` and `name` in the session, and redirect (302) to the saved `next` URL (or `/` if none)

#### Scenario: Successful callback — returning OIDC user
- **WHEN** the OIDC provider redirects to `/auth/callback` for a user already in the local database
- **THEN** the system SHALL update the existing user row (`name` field), store `user_id` in the session, and redirect (302) to the saved `next` URL

#### Scenario: Callback error
- **WHEN** the callback receives an `error` parameter or the code exchange fails
- **THEN** the system SHALL respond with HTTP 401 and an error message

### Requirement: Session-based authentication dependency
The system SHALL provide a `require_auth` FastAPI dependency that resolves the current user from either a Bearer JWT token or a session cookie. The resolved `UserInfo` SHALL include `id` (local user UUID), `username`, `groups` (list of group names). If neither is present, the dependency SHALL redirect browsers to the login page or return HTTP 401 for API clients.

#### Scenario: Authenticated via Bearer JWT
- **WHEN** a request includes a valid `Authorization: Bearer <jwt>` header
- **THEN** the dependency SHALL decode the token, load the user and their groups from the database, and return `UserInfo`

#### Scenario: Authenticated via session (OIDC)
- **WHEN** a request has a valid session with `user_id`
- **THEN** the dependency SHALL load the user and their groups from the database and return `UserInfo`

#### Scenario: Unauthenticated browser request
- **WHEN** a request has no valid token or session and `Accept` includes `text/html`
- **THEN** the dependency SHALL redirect (302) to `/auth/login?next=<current_url>`

#### Scenario: Unauthenticated API request
- **WHEN** a request has no valid token or session and `Accept` does not include `text/html`
- **THEN** the dependency SHALL return HTTP 401 with `{"detail": "Not authenticated"}`
