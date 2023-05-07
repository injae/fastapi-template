from fastapi import APIRouter
from pydantic import BaseModel

from .v1 import router as v1_router

router = APIRouter(prefix="/api")
router.include_router(v1_router, prefix="/v1")


class HealthCheckResponse(BaseModel):
    status: str


@router.get("/health")
async def health() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok")
