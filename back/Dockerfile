# syntax = docker/dockerfile:latest
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

ARG BUILD_DIR=/build
ARG POETRY_VENV_LOCATION=${BUILD_DIR}/.venv
ARG PROJECT_NAME
ARG CACHE_ID_PREFIX
ARG POETRY_VENV_CACHE_ID=${CACHE_ID_PREFIX}-${PROJECT_NAME}-poetry-venv-cache

# Stage: Set up application dependencies
FROM base as build
ARG BUILD_DIR
WORKDIR $BUILD_DIR
ARG POETRY_VERSION=1.6.1
ARG POETRY_VENV_LOCATION
ARG POETRY_INSTALL_WITH="main"
ARG PIP_CACHE_ID=${CACHE_ID_PREFIX}-${PROJECT_NAME}-pip-cache
ARG POETRY_CACHE_ID=${CACHE_ID_PREFIX}-${PROJECT_NAME}-poetry-cache
ARG POETRY_VENV_CACHE_ID
ENV PIP_CACHE_DIR=/pip-cache
ENV POETRY_CACHE_DIR=/poetry-cache
# Install poetry
RUN --mount=type=cache,id=${PIP_CACHE_ID},target=${PIP_CACHE_DIR} \
    pip install \
    --cache-dir ${PIP_CACHE_DIR} --disable-pip-version-check --root-user-action=ignore \
    poetry==${POETRY_VERSION}
# Install python packages
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    --mount=type=cache,id=${POETRY_CACHE_ID},target=${POETRY_CACHE_DIR} \
    --mount=type=cache,id=${POETRY_VENV_CACHE_ID},target=${POETRY_VENV_LOCATION} \
    POETRY_VIRTUALENVS_IN_PROJECT=true poetry install \
    --no-ansi --no-interaction --sync --with=${POETRY_INSTALL_WITH} \
    && touch /BUILD_SUCCEEDED

# Stage: Set up application runtime
FROM base as run
ARG SOURCE_APP_DIR=./app/
ARG POETRY_VENV_CACHE_ID
ARG POETRY_VENV_LOCATION
ENV PATH=${POETRY_VENV_LOCATION}/bin:${PATH}
ENV PYTHONPATH=/app:${PYTHONPATH}
ENV PYTHONUNBUFFERED=1
# Trigger build stage to generate venv cache
COPY --from=build /BUILD_SUCCEEDED /BUILD_SUCCEEDED
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    --mount=type=cache,id=${POETRY_VENV_CACHE_ID},target=/built-venv \
    mkdir -p ${POETRY_VENV_LOCATION} && cp -r /built-venv/* ${POETRY_VENV_LOCATION}
COPY $SOURCE_APP_DIR /app/
WORKDIR /app