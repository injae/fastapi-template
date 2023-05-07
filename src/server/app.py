from fastapi import FastAPI

from .api import router as api_router
from .injector import Container
from .middlewares import RequestResponseLoggingMiddleware


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container  # type: ignore  # noqa: PGH003

    # routers
    app.include_router(api_router)

    # middlewares
    app.add_middleware(RequestResponseLoggingMiddleware)

    return app
