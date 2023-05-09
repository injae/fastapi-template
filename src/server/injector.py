from typing import Annotated

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide
from fastapi import Depends
from server.services.redis import RedisService, redis_session
from server.setting import Setting


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[".api", ".api.v1", ".api.v1.store"],
    )
    config = providers.Configuration(pydantic_settings=[Setting()])

    redis = providers.Resource(redis_session, config.redis)

    redis_service = providers.Factory(RedisService, redis)


RedisService = Annotated[RedisService, Depends(Provide[Container.redis_service])]
