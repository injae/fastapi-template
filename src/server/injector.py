from dependency_injector import containers, providers

from server.services.redis import RedisConfig, RedisService, redis_session


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[".api", ".api.v1", ".api.v1.store"],
    )
    config = providers.Configuration(yaml_files="config.yml")

    redis = providers.Resource(redis_session, RedisConfig())

    redis_service = providers.Factory(RedisService, redis)
