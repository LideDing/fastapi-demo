## Why

The OAuth callback URL is currently inconsistent: the environment configuration (`.env.example`, `set_env.sh`) uses `/oidc/callback` while the actual FastAPI router is mounted at `/auth/callback`. This mismatch causes OAuth callbacks to fail. The decision is to unify all callback URLs to `http://127.0.0.1:8000/auth/callback`.

## What Changes

- Update `OIDC_REDIRECT_URL` in `.env.example` from `http://127.0.0.1:8000/oidc/callback` to `http://127.0.0.1:8000/auth/callback`
- Update `OIDC_REDIRECT_URL` in `set_env.sh` from `http://127.0.0.1:8000/oidc/callback` to `http://127.0.0.1:8000/auth/callback`

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

(none — this is a configuration-only fix, no spec-level behavior changes)

## Impact

- **Configuration files**: `.env.example`, `set_env.sh` — callback URL updated
- **Runtime behavior**: OAuth flow will work correctly once env vars match the actual route
- **No code changes needed**: The router (`/auth/callback`) and service layer are already correct
