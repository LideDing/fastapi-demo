## ADDED Requirements

### Requirement: Callback URL consistency
All configuration files SHALL use `http://127.0.0.1:8000/auth/callback` as the default OIDC redirect URL, matching the actual router path at `/auth/callback`.

#### Scenario: .env.example has correct callback URL
- **WHEN** a developer copies `.env.example` to `.env`
- **THEN** `OIDC_REDIRECT_URL` SHALL be set to `http://127.0.0.1:8000/auth/callback`

#### Scenario: set_env.sh has correct callback URL
- **WHEN** a developer sources `set_env.sh`
- **THEN** `OIDC_REDIRECT_URL` SHALL be exported as `http://127.0.0.1:8000/auth/callback`
