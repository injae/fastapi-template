import json
import sys
import time
from typing import Any, Self

from fastapi import Request, Response
from fastapi.datastructures import Headers
from loguru import logger
from pydantic import BaseModel
from starlette.background import BackgroundTask
from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import Message

MessageType = str | dict[str, Any] | None

logger.remove()
json_log_format = '{{"timestamp":"{time}","level":"{level}", "message":{message}}}'
logger.add(sys.stdout, format=json_log_format, level="INFO")
logger.add(sys.stderr, format=json_log_format, level="ERROR")


class LogSchema(BaseModel):
    took: float
    method: str
    url: str
    request: MessageType
    status_code: int
    content_length: str | None
    response: MessageType


class LargeLogSchema(BaseModel):
    content_type: str | None
    size: int
    message: str = "Body is too large to log"
    ...


LARGE_CONTENT_SIZE = 2048


def body_to_log_message(
    headers: MutableHeaders | Headers,
    body: bytes,
) -> str | dict[str, Any] | None:
    content_type = headers.get("content-type")
    content_size = int(headers.get("content-length", "0"))

    if content_size >= LARGE_CONTENT_SIZE:
        return LargeLogSchema(
            content_type=content_type,
            size=content_size,
        ).json()

    match content_type:
        case "application/json":
            return json.loads(body.decode("utf-8"))
        case _:
            return None if len(body) == 0 else body.decode("utf-8")


def logging_info(log: LogSchema) -> None:
    logger.info(log.json())


async def set_body(req: Request, body: bytes) -> None:
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    req._receive = receive  # noqa: SLF001


def get_took_ms(start_time: float) -> float:
    return (time.perf_counter_ns() - start_time) / 1000000


class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self: Self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start_time = time.perf_counter_ns()
        req_body = await request.body()
        await set_body(request, req_body)
        response = await call_next(request)

        res_body = b""
        async for chunk in response.body_iterator:  # type: ignore  # noqa: PGH003
            res_body += chunk

        task = BackgroundTask(
            logging_info,
            LogSchema(
                took=get_took_ms(start_time),
                method=request.method,
                url=request.url.path,
                request=body_to_log_message(request.headers, req_body),
                content_length=response.headers.get("content-length"),
                status_code=response.status_code,
                response=body_to_log_message(response.headers, res_body),
            ),
        )
        return Response(
            res_body,
            status_code=response.status_code,
            headers=response.headers,
            background=task,
        )
