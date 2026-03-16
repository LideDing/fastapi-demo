from urllib.parse import quote

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.models.auth import UserInfo
from app.services.user_auth import decode_access_token, get_user_with_groups


class _RedirectToLogin(Exception):
    def __init__(self, login_url: str):
        self.login_url = login_url


def redirect_to_login_handler(
    request: Request, exc: "_RedirectToLogin"
) -> RedirectResponse:
    return RedirectResponse(url=exc.login_url, status_code=302)


async def require_auth(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> UserInfo:
    # 1. Try Bearer JWT first
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
        try:
            user_id = decode_access_token(token)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        result = await get_user_with_groups(db, user_id)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        user, groups = result
        return UserInfo(
            id=str(user.id),
            sub=str(user.id),
            name=user.username,
            groups=groups,
        )

    # 2. Try session (OIDC flow) — user_id stored after OIDC callback
    session_user_id = request.session.get("user_id")
    if session_user_id:
        result = await get_user_with_groups(db, session_user_id)
        if result is not None:
            user, groups = result
            return UserInfo(
                id=str(user.id),
                sub=str(user.id),
                name=user.username,
                groups=groups,
            )

    # 3. Not authenticated — redirect browsers, 401 for API clients
    accept = request.headers.get("Accept", "")
    if "text/html" in accept:
        current_url = str(request.url.path)
        if request.url.query:
            current_url += f"?{request.url.query}"
        login_url = f"/auth/login?next={quote(current_url)}"
        raise _RedirectToLogin(login_url)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )


async def require_admin(user: UserInfo = Depends(require_auth)) -> UserInfo:
    if "admin" not in user.groups:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user
