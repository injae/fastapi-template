from dependency_injector.wiring import inject
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from server.injector import RedisService

router = APIRouter(prefix="/store")


class RequestStoreData(BaseModel):
    key: str
    name: str


class ResponseStoreData(BaseModel):
    name: str


@router.post("/")
@inject
async def store_data(
    req: RequestStoreData,
    redis_service: RedisService,
) -> ResponseStoreData:
    try:
        await redis_service.set_str(req.key, req.name)
    except Exception as e:
        raise HTTPException(status_code=500) from e

    return ResponseStoreData(name=req.name)
