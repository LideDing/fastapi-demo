from fastapi import APIRouter

from fastapi import Request
from app.models.hello import HelloResponse
from app.services.hello import hello_world

router = APIRouter()

# hello需要获取访问IP并返回
@router.get("/hello", response_model=HelloResponse)
async def hello(request: Request) -> dict[str, str]:
    host = request.client.host if request.client else "unknown"
    return hello_world(host)
