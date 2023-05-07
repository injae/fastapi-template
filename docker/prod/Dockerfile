FROM python:3.11.3-slim-bullseye as base

ENV DEBIAN_FRONTEND="noninteractive"

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       build-essential \
    && rm -rf /var/lib/apt/lists/*


FROM base as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

ARG POETRY_VERSION=1.3.2

RUN pip install --no-cache-dir poetry==$POETRY_VERSION

COPY ./pyproject.toml ./poetry.lock /app/

WORKDIR /app

# hadolint ignore=SC2094
RUN poetry export -f requirements.txt --without-hashes --no-interaction --no-ansi > requirements.txt

FROM base as final

ENV FASTAPI_ENV=production \
    WORKER=4 \
    PORT=80

WORKDIR /app

COPY --from=builder /app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN echo gunicorn server.main:app --workers ${WORKER} --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT} > /app/start.sh \
    && chmod +x /app/start.sh

COPY src/server /app/server

EXPOSE ${PORT}

CMD ["/bin/bash", "-c", "./start.sh"]
