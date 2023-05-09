from pydantic import BaseSettings
from server.services.redis import RedisConfig


class Setting(BaseSettings):
    redis: RedisConfig = RedisConfig()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
