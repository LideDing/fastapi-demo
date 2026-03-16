import logging
import secrets

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.services.auth import (
    exchange_code_for_token,
    fetch_userinfo,
    get_authorization_url,
)
from app.services.user_auth import upsert_oidc_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def login(request: Request, next: str = "/") -> RedirectResponse:
    state = secrets.token_urlsafe(32)
    request.session["oauth_state"] = state
    request.session["oauth_next"] = next

    authorization_url = await get_authorization_url(state)
    return RedirectResponse(url=authorization_url, status_code=302)


@router.get("/callback")
async def callback(
    request: Request,
    db: AsyncSession = Depends(get_db),
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
) -> RedirectResponse:
    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"OIDC provider error: {error}",
        )

    if code is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization code",
        )

    saved_state = request.session.pop("oauth_state", None)
    if saved_state is None or saved_state != state:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid state parameter",
        )

    try:
        token = await exchange_code_for_token(code, state)
    except Exception:
        logger.exception("Failed to exchange code for token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to exchange authorization code",
        )

    access_token = token.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access token received",
        )

    try:
        userinfo = await fetch_userinfo(access_token)
    except Exception:
        logger.exception("Failed to fetch user info")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to fetch user info",
        )

    sub = userinfo.get("sub", "")
    name = userinfo.get("name", sub)

    # Upsert into local users table
    try:
        user = await upsert_oidc_user(db, sub=sub, name=name)
    except Exception:
        logger.exception("Failed to upsert OIDC user")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sync user",
        )

    # Store local user_id in session
    request.session["user_id"] = str(user.id)

    next_url = request.session.pop("oauth_next", "/")
    return RedirectResponse(url=next_url, status_code=302)


@router.get("/logout")
async def logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse(url="/health", status_code=302)
