from collections.abc import AsyncIterator, Awaitable
from typing import Self

from pydantic.dataclasses import dataclass

from redis import asyncio as aioredis


@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379
    username: str | None = None
    password: str | None = None


async def redis_session(config: RedisConfig) -> AsyncIterator[aioredis.Redis]:
    session = aioredis.from_url(
        f"redis://{config.host}:{config.port}",
        username=config.username,
        password=config.password,
        encoding="utf-8",
    )
    yield session
    await session.close()


class RedisService:
    def __init__(self: Self, redis: aioredis.Redis) -> None:
        self._redis: aioredis.Redis = redis

    async def set_str(self: Self, key: str, value: str) -> bool | None:
        return await self._redis.set(key, value)

    async def get_str(self: Self, key: str) -> str | None:
        return await self._redis.get(key)
