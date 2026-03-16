## 1. Cleanup Old Implementation

- [x] 1.1 Remove `python-jose[cryptography]` and `cachetools` from `pyproject.toml` dependencies
- [x] 1.2 Add `authlib` and `itsdangerous` to `pyproject.toml` dependencies (keep `httpx`)
- [x] 1.3 Replace OIDC settings in `app/config.py` with new fields: `oidc_issuer_url`, `oidc_client_id`, `oidc_client_secret`, `oidc_redirect_url`, `oidc_scopes`, and `secret_key`

## 2. Auth Service (OIDC Client)

- [x] 2.1 Rewrite `app/services/auth.py` — set up `authlib` OAuth client with TAI discovery, implement `get_authorization_url()`, `exchange_code_for_token()`, and `fetch_userinfo()` functions
- [x] 2.2 Update `app/models/auth.py` — replace `TokenPayload` with `UserInfo` model (sub, name, and optional extra fields)

## 3. Auth Dependency

- [x] 3.1 Rewrite `app/dependencies/auth.py` — `require_auth` checks session for user info, redirects to `/oidc/login?next=<current_url>` if not logged in

## 4. OIDC Routes

- [x] 4.1 Create `app/routers/oidc.py` with `GET /oidc/login` (saves next URL in session, redirects to TAI authorize endpoint)
- [x] 4.2 Add `GET /oidc/callback` route (exchanges code for token, fetches userinfo, stores in session, redirects to saved next URL)
- [x] 4.3 Add `GET /oidc/logout` route (clears session, redirects to `/`)

## 5. App Integration

- [x] 5.1 Add `SessionMiddleware` to `app/main.py` with `APP_SECRET_KEY`
- [x] 5.2 Register `oidc` router in `app/main.py`
- [x] 5.3 Update `app/routers/hello.py` to use session-based `require_auth` dependency

## 6. Testing

- [x] 6.1 Update unit tests for the new session-based auth dependency (authenticated session, missing session redirect)
- [x] 6.2 Update integration tests: `/hello` redirects when unauthenticated, `/health` remains public, `/oidc/login` redirects to provider, `/oidc/logout` clears session
