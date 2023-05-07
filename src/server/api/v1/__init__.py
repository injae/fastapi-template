from fastapi import APIRouter

from .store import router as store_router

router = APIRouter()

router.include_router(store_router)
