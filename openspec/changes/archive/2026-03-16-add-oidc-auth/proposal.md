## Why

The application currently exposes all endpoints without authentication. We need OIDC-based authentication using the TAI Auth Center (Authorization Code Flow) so that protected endpoints (like `/hello`) require a logged-in user session, while health-check endpoints (`/health`) remain publicly accessible for monitoring.

## What Changes

- Implement full OIDC Authorization Code Flow with TAI Auth Center as the provider
- Add `/oidc/callback` route to handle the authorization code → token exchange
- Add `/oidc/login` and `/oidc/logout` routes for explicit login/logout
- Add server-side session management via signed cookies
- Protect `/hello` endpoint — unauthenticated users are redirected to TAI login page
- Keep `/health` endpoint public (no authentication required)
- Remove existing JWT/JWKS local validation code (replaced by session-based auth)
- Add `authlib` and `itsdangerous` dependencies

## Capabilities

### New Capabilities
- `oidc-auth`: OIDC Authorization Code Flow with session-based authentication, including login/callback/logout routes and a reusable FastAPI dependency for protecting endpoints

### Modified Capabilities

_(none — no existing spec-level requirements are changing)_

## Impact

- **Code**: Rewrite `app/services/auth.py` (OIDC client logic), `app/models/auth.py` (session/user models), `app/dependencies/auth.py` (session-based auth dependency), new `app/routers/oidc.py` (login/callback/logout routes), update `app/routers/hello.py`
- **Config**: Replace `APP_OIDC_*` env vars with `OIDC_ISSUER_URL`, `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, `OIDC_REDIRECT_URL`, `OIDC_SCOPES`
- **Dependencies**: Replace `python-jose`/`cachetools` with `authlib`, add `itsdangerous` for signed cookies, keep `httpx`
- **APIs**: `/hello` redirects to login when unauthenticated; `/health` unchanged; new `/oidc/login`, `/oidc/callback`, `/oidc/logout` routes
