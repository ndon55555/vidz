# syntax = docker/dockerfile:latest
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

# Stage: Set up application dependencies
FROM base as build
WORKDIR /build
ARG POETRY_VERSION=1.6.1
ENV PIP_CACHE_DIR=/pip-cache
ENV POETRY_CACHE_DIR=/poetry-cache

RUN --mount=type=cache,id=vidz-pip-cache,target=${PIP_CACHE_DIR} \
    pip --cache-dir ${PIP_CACHE_DIR} install poetry==${POETRY_VERSION}

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    --mount=type=cache,id=vidz-poetry-cache,target=${POETRY_CACHE_DIR} \
    POETRY_VIRTUALENVS_IN_PROJECT=true poetry install

# Stage: Set up application runtime
FROM base as run
ARG APP_DIR=./app/
ENV PATH=/venv/bin:${PATH}
ENV PYTHONPATH=/app:${PYTHONPATH}
COPY --from=build /build/.venv/ /venv
COPY $APP_DIR /app/
