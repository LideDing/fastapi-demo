import os

# Set env vars before any app imports
os.environ.setdefault("OIDC_ISSUER_URL", "https://idp.example.com/oauth2/")
os.environ.setdefault("OIDC_CLIENT_ID", "test-client-id")
os.environ.setdefault("OIDC_CLIENT_SECRET", "test-client-secret")
os.environ.setdefault("OIDC_REDIRECT_URL", "http://127.0.0.1:8000/oidc/callback")
os.environ.setdefault("OIDC_SCOPES", "openid,profile")
os.environ.setdefault("APP_SECRET_KEY", "test-secret-key-for-sessions")
