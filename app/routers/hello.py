from fastapi import APIRouter, Depends, Request

from app.dependencies.auth import require_auth
from app.models.auth import UserInfo
from app.models.hello import HelloResponse
from app.services.hello import hello_world

router = APIRouter()


@router.get("/hello", response_model=HelloResponse)
async def hello(
    request: Request,
    _user: UserInfo = Depends(require_auth),
) -> dict[str, str]:
    host = request.client.host if request.client else "unknown"
    return hello_world(host)
