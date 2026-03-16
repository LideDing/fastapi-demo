import os

# Set env vars before any app imports
os.environ.setdefault("OIDC_ISSUER_URL", "https://idp.example.com/oauth2/")
os.environ.setdefault("OIDC_CLIENT_ID", "test-client-id")
os.environ.setdefault("OIDC_CLIENT_SECRET", "test-client-secret")
os.environ.setdefault("OIDC_REDIRECT_URL", "http://127.0.0.1:8000/auth/callback")
os.environ.setdefault("OIDC_SCOPES", "openid,profile")
os.environ.setdefault("APP_SECRET_KEY", "test-secret-key-for-sessions")
os.environ.setdefault(
    "APP_DB_URL",
    "postgresql+asyncpg://postgres:mysecretpassword@localhost:5433/fastapi_demo",
)
os.environ.setdefault("APP_JWT_SECRET", "test-jwt-secret-for-unit-tests")
