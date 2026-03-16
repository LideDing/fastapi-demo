## Context

The FastAPI application serves `/health` and `/hello` endpoints. We need OIDC authentication using TAI Auth Center as the identity provider, via the Authorization Code Flow. Users access the app through a browser. When unauthenticated, they are redirected to TAI's login page and returned to the original page after login.

The OIDC provider is TAI Auth Center:
- Discovery: `https://tai.it.tencent.com/api/auth-center/oauth2/.well-known/openid-configuration`
- Authorization, token, userinfo, and introspection endpoints are available via discovery.

The app follows a router/service separation pattern with pydantic-settings configuration.

## Goals / Non-Goals

**Goals:**
- Implement Authorization Code Flow: redirect → login → callback → session
- Server-side session via signed cookies (single-instance deployment)
- Protect `/hello` with login-required; redirect unauthenticated users to TAI login
- Keep `/health` public
- Provide `/oidc/login`, `/oidc/callback`, `/oidc/logout` routes
- Remember the original URL so users return to it after login

**Non-Goals:**
- Token refresh (session-based, re-login on expiry is acceptable)
- Multi-instance session sharing (no Redis, server-side cookie is sufficient)
- Role-based access control (RBAC)
- API-to-API authentication (this is browser-based only)

## Decisions

### 1. OIDC client library: `authlib`

**Choice**: Use `authlib` with its `AsyncOAuth2Client` / Starlette integration for the Authorization Code Flow.

**Rationale**: `authlib` is the de facto standard for OAuth2/OIDC in Python ASGI apps. It handles discovery, authorization URL generation, token exchange, and userinfo retrieval. It integrates well with Starlette (FastAPI's base). Alternative `httpx-oauth` is lighter but `authlib` provides better OIDC discovery support.

### 2. Session management: Starlette `SessionMiddleware` with signed cookies

**Choice**: Use Starlette's built-in `SessionMiddleware` which stores session data in a signed cookie using `itsdangerous`.

**Rationale**: Simple, no external dependencies (Redis, database). Fits the single-instance deployment model. Cookie is signed (tamper-proof) but not encrypted — only stores non-sensitive data (user sub, name). Session size is limited (~4KB) but sufficient for basic user info.

### 3. Configuration: OIDC-specific env vars (no APP_ prefix)

**Choice**: Use the env vars as provided by the user:
- `OIDC_ISSUER_URL` — TAI OAuth2 base URL
- `OIDC_CLIENT_ID` — Application ID
- `OIDC_CLIENT_SECRET` — Application secret
- `OIDC_REDIRECT_URL` — Callback URL (`http://127.0.0.1:8000/oidc/callback`)
- `OIDC_SCOPES` — Requested scopes (`openid,profile`)

These use the `OIDC_` prefix (not `APP_OIDC_`) to match the user's existing env var naming. Add a separate pydantic-settings model or nest within existing Settings with `env_prefix=""` override.

### 4. Auth flow and routes

```
GET /hello (protected)
  │
  ├─ Has session with user info? → serve response
  │
  └─ No session? → 302 to /oidc/login?next=/hello

GET /oidc/login
  │
  ├─ Save ?next URL in session
  └─ 302 to TAI authorize URL
       (with client_id, redirect_uri, scope, state)

GET /oidc/callback?code=...&state=...
  │
  ├─ Exchange code for tokens (POST /token)
  ├─ Fetch userinfo (GET /userinfo) or decode id_token
  ├─ Store user info in session
  └─ 302 to saved ?next URL (default: /)

GET /oidc/logout
  │
  ├─ Clear session
  └─ 302 to / (or TAI end_session_endpoint if available)
```

### 5. File layout

- `app/services/auth.py` — OIDC client setup, token exchange, userinfo fetch
- `app/models/auth.py` — `UserInfo` model (sub, name, etc.)
- `app/dependencies/auth.py` — `require_auth` dependency (checks session, redirects if not logged in)
- `app/routers/oidc.py` — `/oidc/login`, `/oidc/callback`, `/oidc/logout` routes
- `app/config.py` — Add OIDC settings
- `app/main.py` — Add `SessionMiddleware`, register oidc router

### 6. Secret key for session signing

**Choice**: Add `APP_SECRET_KEY` env var for `SessionMiddleware`. Default to a random value in dev (logged as warning), required in production.

**Rationale**: `SessionMiddleware` needs a secret to sign cookies. Must be stable across restarts to avoid invalidating sessions.

## Risks / Trade-offs

- **[Cookie size limit]** → ~4KB. Mitigation: only store essential user info (sub, name), not full tokens.
- **[No token refresh]** → Session expires when cookie expires. Mitigation: set reasonable cookie max_age; user re-logs in. Acceptable for this use case.
- **[Secret key management]** → If `APP_SECRET_KEY` is not set, sessions are insecure. Mitigation: log a warning, require it in production.
- **[OIDC provider downtime]** → Login flow breaks if TAI is down. Mitigation: existing sessions continue to work; only new logins fail.
