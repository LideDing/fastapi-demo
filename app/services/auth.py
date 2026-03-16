import logging

import httpx
from authlib.integrations.httpx_client import AsyncOAuth2Client

from app.config import oidc_settings

logger = logging.getLogger(__name__)

_discovery_cache: dict | None = None


async def _get_discovery() -> dict:
    global _discovery_cache
    if _discovery_cache is not None:
        return _discovery_cache

    issuer = oidc_settings.issuer_url.rstrip("/")
    url = f"{issuer}/.well-known/openid-configuration"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=10)
        resp.raise_for_status()
        _discovery_cache = resp.json()
        logger.info("OIDC discovery document fetched")
        return _discovery_cache


def _create_oauth_client() -> AsyncOAuth2Client:
    return AsyncOAuth2Client(
        client_id=oidc_settings.client_id,
        client_secret=oidc_settings.client_secret,
        redirect_uri=oidc_settings.redirect_url,
        token_endpoint_auth_method="client_secret_post",
    )


async def get_authorization_url(state: str) -> str:
    discovery = await _get_discovery()
    authorize_endpoint = discovery["authorization_endpoint"]
    scopes = oidc_settings.scopes.replace(",", " ")

    client = _create_oauth_client()
    uri, _state = client.create_authorization_url(
        authorize_endpoint,
        scope=scopes,
        state=state,
    )
    return uri


async def exchange_code_for_token(code: str, state: str) -> dict:
    discovery = await _get_discovery()
    token_endpoint = discovery["token_endpoint"]

    client = _create_oauth_client()
    try:
        token = await client.fetch_token(
            token_endpoint,
            code=code,
            grant_type="authorization_code",
        )
    except Exception as e:
        logger.error("exchange_code_for_token failed: %s", e, exc_info=True)
        raise
    logger.debug("token response: %s", token)
    return token


async def fetch_userinfo(access_token: str) -> dict:
    discovery = await _get_discovery()
    userinfo_endpoint = discovery["userinfo_endpoint"]

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
