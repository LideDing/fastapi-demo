## 1. Update configuration files

- [ ] 1.1 Update `OIDC_REDIRECT_URL` in `.env.example` from `http://127.0.0.1:8000/oidc/callback` to `http://127.0.0.1:8000/auth/callback`
- [ ] 1.2 Update `OIDC_REDIRECT_URL` in `set_env.sh` from `http://127.0.0.1:8000/oidc/callback` to `http://127.0.0.1:8000/auth/callback`

## 2. Verification

- [ ] 2.1 Verify no other files reference the old `/oidc/callback` path
