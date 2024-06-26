FROM python:3.12.0-slim-bullseye

ARG APP_HOME=/app
ARG BUILD_ENVIRONMENT=production
ARG UID=1000
ARG GID=1000

ENV DJANGO_ENV ${BUILD_ENVIRONMENT}
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.2.2
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_HOME='/usr/local'
ENV POETRY_CACHE_DIR='/tmp/poetry_cache'

WORKDIR ${APP_HOME}

RUN groupadd -g "${GID}" -r web \
  && useradd -d $APP_HOME -g web -l -r -u "${UID}" web \
  && chown web:web -R $APP_HOME \
  # Static files:
  && mkdir -p '/var/www/static' \
  && chown -R web:web '/var/www/static'


RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # Other tools \
  curl bash \
  wget gnupg2 \
  gettext \
  wait-for-it \
  brotli

RUN echo "deb http://apt.postgresql.org/pub/repos/apt bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget -qO - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
RUN apt update
RUN apt-get remove -y wget gnupg2
RUN apt-get -y install postgresql-client-15

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
  && apt-get install --no-install-recommends -y nodejs \
  && npm install -g npm@9.1.2

# Cleaning cache:
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN curl -sSL 'https://install.python-poetry.org' | POETRY_HOME='/usr/local' python - \
  && poetry --version

COPY --chown=web:web ./poetry.lock ./pyproject.toml ${APP_HOME}/

RUN cd ${APP_HOME} && poetry config virtualenvs.create false \
  && poetry install --without dev --no-interaction --no-ansi \
  && rm -rf ${POETRY_CACHE_DIR}

COPY --chown=web:web ./package-lock.json ./package.json ${APP_HOME}/

RUN npm install

COPY --chown=web:web . ${APP_HOME}/

RUN npm run build && rm -rf node_modules

COPY --chown=web:web ./compose/production/app/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=web:web ./compose/production/app/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


COPY --chown=web:web ./compose/production/app/celery/worker/start /start-celery-workers
RUN sed -i 's/\r$//g' /start-celery-workers
RUN chmod +x /start-celery-workers


COPY --chown=web:web ./compose/production/app/celery/beat/start /start-celery-beat
RUN sed -i 's/\r$//g' /start-celery-beat
RUN chmod +x /start-celery-beat


COPY --chown=web:web ./compose/production/app/celery/flower/start /start-celery-flower
RUN sed -i 's/\r$//g' /start-celery-flower
RUN chmod +x /start-celery-flower

RUN chown -R web:web ${APP_HOME}

USER web

ENTRYPOINT ["/entrypoint"]
