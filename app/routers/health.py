from fastapi import APIRouter

from app.models.health import HealthResponse
from app.services.health import check_health

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> dict[str, str]:
    return check_health()
