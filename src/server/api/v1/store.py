from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from server.injector import Container
from server.services.redis import RedisService

router = APIRouter(prefix="/store")


class RequestStoreData(BaseModel):
    key: str
    name: str


class ResponseStoreData(BaseModel):
    name: str


DependRedisService = Annotated[RedisService, Depends(Provide[Container.redis_service])]


@router.post("/")
@inject
async def store_data(
    req: RequestStoreData,
    store: DependRedisService,
) -> ResponseStoreData:
    try:
        await store.set_str(req.key, req.name)
    except Exception as e:
        raise HTTPException(status_code=500) from e

    return ResponseStoreData(name=req.name)
