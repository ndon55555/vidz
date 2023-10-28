# syntax = docker/dockerfile:latest
ARG APP_DIR=/app

ARG NODE_VERSION=20.9.0
FROM node:${NODE_VERSION}-slim as build
ARG PROJECT_NAME
ARG CACHE_ID_PREFIX
ARG APP_DIR
ENV PNPM_HOME="/pnpm"
ENV PATH=${PNPM_HOME}:${PATH}
RUN corepack enable
ARG PNPM_CACHE_ID=${CACHE_ID_PREFIX}-${PROJECT_NAME}-pnpm-cache
ARG NODE_MODULES_CACHE_ID=${CACHE_ID_PREFIX}-${PROJECT_NAME}-node-modules-cache
ARG NODE_MODULES_CACHE=${APP_DIR}/node_modules
WORKDIR ${APP_DIR}
COPY . ${APP_DIR}
RUN --mount=type=cache,id=pnpm,target=${PNPM_HOME} \
    --mount=type=cache,id=${NODE_MODULES_CACHE_ID},target=${NODE_MODULES_CACHE} \
    pnpm install --frozen-lockfile \
    && pnpm run build

FROM nginx:1.25 as prod-run
ARG APP_DIR
COPY --from=build ${APP_DIR}/dist /usr/share/nginx/html
