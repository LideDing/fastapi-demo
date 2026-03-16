## Context

The application uses OIDC authentication with the router mounted at `/auth` prefix. The callback route is `/auth/callback`. However, the environment configuration files (`.env.example` and `set_env.sh`) still reference the old path `/oidc/callback`, creating a mismatch that breaks the OAuth flow.

## Goals / Non-Goals

**Goals:**
- Align all callback URL references to `http://127.0.0.1:8000/auth/callback`
- Ensure `.env.example` and `set_env.sh` are consistent with the actual router path

**Non-Goals:**
- Changing the router prefix or application code
- Modifying the OIDC provider configuration (that is done externally)

## Decisions

**Update config files only**: The router is already correctly at `/auth/callback`. Only the environment variable defaults in `.env.example` and `set_env.sh` need updating from `/oidc/callback` to `/auth/callback`. No code changes required.

## Risks / Trade-offs

- [Risk] Existing deployments using old env values → Mitigation: Users must update their `OIDC_REDIRECT_URL` env var and the corresponding redirect URI registered with their OIDC provider.
