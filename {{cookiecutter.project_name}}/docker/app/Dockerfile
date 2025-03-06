ARG APP_HOME="/app"

# --------------------------------------------------------------
# Build frontend asset files
# --------------------------------------------------------------
FROM node:22-slim as frontend_builder

ARG APP_HOME

ENV APP_HOME="$APP_HOME"
ENV VITE_APP_OUTPUT_DIR="dist"


COPY package.json package-lock.json ./

RUN npm install

COPY . ${APP_HOME}/

WORKDIR $APP_HOME

RUN npm run build

# --------------------------------------------------------------
# Builder
# --------------------------------------------------------------
FROM python:3.13.1-slim-bookworm as builder

ARG APP_HOME
ENV APP_HOME="$APP_HOME"
ENV VIRTUAL_ENV_PATH="$APP_HOME/.venv/"
ENV DIST_DIR="$APP_HOME/dist/"
ENV UV_PROJECT_ENVIRONMENT="${VIRTUAL_ENV_PATH}"

RUN apt-get update && apt-get install --no-install-recommends -y \
  # Other tools \
  gettext \
  dos2unix \
  tini \
  # Cleaning cache:
  && apt-get purge -y --auto-remove \
  && apt-get autoclean \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

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

# --------------------------------------------------------------
# Testing build
# --------------------------------------------------------------
FROM builder as tester

ENV PYTHONPATH="$VIRTUAL_ENV_PATH/lib/python3.13/site-packages:$PYTHON_PATH" 
ENV TEST=true

COPY --from=builder ${VIRTUAL_ENV_PATH} ${VIRTUAL_ENV_PATH}

RUN  pip install \
  pytest \
  pytest-sugar \
  pytest-django \
  pytest-cov \
  coverage \
  pytest-xdist \
  pytest-mock \
  pytest-env \
  mixer

COPY --from=frontend_builder ${DIST_DIR} ${DIST_DIR}

COPY . ${APP_HOME}/

WORKDIR $APP_HOME

CMD ["pytest"]

# --------------------------------------------------------------
# Production build
# --------------------------------------------------------------
FROM gcr.io/distroless/base-debian12:nonroot as production

ARG CHIPSET_ARCH=aarch64
ARG APP_HOME

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE=1

ENV APP_HOME="$APP_HOME"
ENV VIRTUAL_ENV_PATH="$APP_HOME/.venv"
ENV DIST_DIR="$APP_HOME/dist/"
ENV PATH="$VIRTUAL_ENV_PATH/bin:$PATH"
ENV VITE_APP_OUTPUT_DIR="dist"
ENV PYTHONPATH="/usr/lib/python3.13:$VIRTUAL_ENV_PATH/lib/python3.13/site-packages:$PYTHON_PATH" 
ENV PYTHONHOME="/usr"
ENV LD_LIBRARY_PATH="/lib:/usr/lib:/usr/local/lib:$VIRTUAL_ENV_PATH/lib:$LD_LIBRARY_PATH"

# COPY --from=builder /python-libs /
COPY --from=builder /usr/local/bin/python* /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.13 /usr/lib/python3.13
COPY --from=builder /usr/local/lib/libpython3.13.so.1.0 /usr/local/lib/libpython3.13.so.1.0

COPY --from=builder /etc/ld.so.cache /etc/ld.so.cache
COPY --from=builder /lib/${CHIPSET_ARCH}-linux-gnu/ /lib/${CHIPSET_ARCH}-linux-gnu/

COPY --from=builder /usr/bin/tini /usr/bin/tini
COPY --from=builder /usr/bin/gettext /usr/bin/gettext

USER nonroot

COPY --chown=nonroot:nonroot --from=builder ${VIRTUAL_ENV_PATH} ${VIRTUAL_ENV_PATH}

COPY --chown=nonroot:nonroot --from=frontend_builder ${DIST_DIR} ${DIST_DIR}

COPY --chown=nonroot:nonroot . ${APP_HOME}

WORKDIR $APP_HOME

ENTRYPOINT ["/usr/bin/tini", "--"]