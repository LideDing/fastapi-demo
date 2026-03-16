from urllib.parse import quote

from fastapi import Request
from fastapi.responses import RedirectResponse

from app.models.auth import UserInfo


async def require_auth(request: Request) -> UserInfo:
    user_data = request.session.get("user")
    if user_data is None:
        current_url = str(request.url.path)
        if request.url.query:
            current_url += f"?{request.url.query}"
        login_url = f"/oidc/login?next={quote(current_url)}"
        raise _RedirectToLogin(login_url)

    return UserInfo(**user_data)


class _RedirectToLogin(Exception):
    def __init__(self, login_url: str):
        self.login_url = login_url


def redirect_to_login_handler(
    request: Request, exc: _RedirectToLogin
) -> RedirectResponse:
    return RedirectResponse(url=exc.login_url, status_code=302)
