# Build frontend asset files
FROM node:22-slim as frontend_builder

ENV APP_HOME="/app"
ENV VITE_APP_OUTPUT_DIR="dist"

WORKDIR $APP_HOME

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

FROM python:3.12.0-slim-bookworm as python_base

ENV APP_HOME="/app"
ENV VIRTUAL_ENV_PATH="$APP_HOME/.venv/"
ENV DIST_DIR="$APP_HOME/dist/"
ENV PATH="$VIRTUAL_ENV_PATH/bin:$PATH"
ENV VITE_APP_OUTPUT_DIR="dist"

WORKDIR $APP_HOME

# Use poetry to get all the deps
FROM python_base as python_deps

ENV POETRY_VERSION=1.8.3
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_HOME='/usr/local'
ENV POETRY_VIRTUALENVS_PATH="${VIRTUAL_ENV_PATH}"
ENV POETRY_CACHE_DIR='/tmp/poetry_cache'

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock ./

RUN touch README.md
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --only=main --no-root

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
  lsb-release \
  ca-certificates \
  curl \
  gnupg2 \
  gettext \
  dos2unix \
  tini \
  # Cleaning cache:
  && apt-get remove curl -y \
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
