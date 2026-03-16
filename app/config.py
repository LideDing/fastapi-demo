import secrets

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "APP_"}

    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = ["*"]
    secret_key: str = secrets.token_urlsafe(32)


class OIDCSettings(BaseSettings):
    model_config = {"env_prefix": "OIDC_"}

    issuer_url: str
    client_id: str
    client_secret: str
    redirect_url: str
    scopes: str = "openid,profile"


settings = Settings()
oidc_settings = OIDCSettings()
