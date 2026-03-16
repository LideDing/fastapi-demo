#!/buin/bash

export OIDC_ISSUER_URL=https://tai.it.tencent.com/api/auth-center/oauth2/
export OIDC_CLIENT_ID=lide_gin_test
export OIDC_CLIENT_SECRET=SCFTW688ECFESSDUCBXZOCEVEVWZVFQN
export OIDC_REDIRECT_URL=http://127.0.0.1:8000/oidc/callback
export OIDC_SCOPES=openid,profile
# export APP_SECRET_KEY=<a-stable-random-string>