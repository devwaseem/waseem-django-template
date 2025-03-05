# Build frontend asset files
FROM node:22-slim as frontend_builder

ENV APP_HOME="/app"
ENV VITE_APP_OUTPUT_DIR="dist"

WORKDIR $APP_HOME

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

FROM python:3.13.1-slim-bookworm as python_base


ENV APP_HOME="/app"
ENV VIRTUAL_ENV_PATH="$APP_HOME/.venv/"
ENV DIST_DIR="$APP_HOME/dist/"
ENV PATH="$VIRTUAL_ENV_PATH/bin:$PATH"
ENV VITE_APP_OUTPUT_DIR="dist"

WORKDIR $APP_HOME

# Use poetry to get all the deps
FROM python_base as python_deps

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

#https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy
# https://docs.astral.sh/uv/guides/integration/docker/#non-editable-installs
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --no-dev --frozen --no-install-project --no-editable

RUN find $VIRTUAL_ENV_PATH -type d -name '__pycache__' -exec rm -r {} +
RUN find $VIRTUAL_ENV_PATH -name '*.dist-info' -type d -exec rm -r {} +
RUN find $VIRTUAL_ENV_PATH -name '*.egg-info' -type d -exec rm -r {} +

# Production build
FROM python_base as production

ARG UID=1000
ARG GID=1000
ARG APP_NAME="web"

ENV UID=${UID:-1000}
ENV GID=${GID:-1000}
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE=1

RUN groupadd -g "${GID}" $APP_NAME || exit 0
RUN useradd -d $APP_HOME -g "${GID}" -u "${UID}" -l -r $APP_NAME  || exit 0

RUN mkdir -p '/var/www/static' \
  && chown -R $APP_NAME:$APP_NAME '/var/www/static'

USER root

RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Other tools \
  gettext \
  dos2unix \
  tini \
  # Cleaning cache:
  && apt-get purge -y --auto-remove \
  && apt-get autoclean \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

COPY --chown=$APP_NAME:$APP_NAME --from=python_deps ${VIRTUAL_ENV_PATH} ${VIRTUAL_ENV_PATH}

COPY --chown=$APP_NAME:$APP_NAME --from=frontend_builder ${DIST_DIR} ${DIST_DIR}

COPY --chown=$APP_NAME:$APP_NAME . .

COPY --chown=$APP_NAME:$APP_NAME docker-entrypoint.sh /docker-entrypoint.sh
RUN dos2unix /docker-entrypoint.sh && \
  chmod a+x /docker-entrypoint.sh

USER $APP_NAME

ENTRYPOINT ["/usr/bin/tini", "--", "/bin/bash", "/docker-entrypoint.sh"]
