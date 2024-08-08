#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

APP_HOME="${APP_HOME:-/app}"

# Database environment variables used to check the Postgresql connection.
DATABASE_USER="${DATABASE_USER:-baserow}"
DATABASE_HOST="${DATABASE_HOST:-db}"
DATABASE_PORT="${DATABASE_PORT:-5432}"
DATABASE_NAME="${DATABASE_NAME:-baserow}"
DATABASE_PASSWORD="${DATABASE_PASSWORD:-baserow}"
DATABASE_OPTIONS="${DATABASE_OPTIONS:-}"
# Or you can provide a Postgresql connection url
DATABASE_URL="${DATABASE_URL:-}"

POSTGRES_STARTUP_CHECK_ATTEMPTS="${POSTGRES_STARTUP_CHECK_ATTEMPTS:-5}"
MIGRATE_ON_STARTUP=${MIGRATE_ON_STARTUP:-true}

postgres_ready() {
  if [ -z "$DATABASE_URL" ]; then
    DATABASE_NAME=$DATABASE_NAME \
      DATABASE_USER=$DATABASE_USER \
      DATABASE_HOST=$DATABASE_HOST \
      DATABASE_PORT=$DATABASE_PORT \
      DATABASE_PASSWORD=$DATABASE_PASSWORD \
      DATABASE_OPTIONS=$DATABASE_OPTIONS \
      python3 <<END
import sys
import psycopg2
import json
import os
DATABASE_NAME=os.getenv('DATABASE_NAME')
DATABASE_USER=os.getenv('DATABASE_USER')
DATABASE_HOST=os.getenv('DATABASE_HOST')
DATABASE_PORT=os.getenv('DATABASE_PORT')
DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD')
DATABASE_OPTIONS=os.getenv('DATABASE_OPTIONS')
try:
    options = json.loads(DATABASE_OPTIONS or "{}")
    psycopg2.connect(
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        **options
    )
except Exception as e:
    print(f"Error: Failed to connect to the postgresql database at {DATABASE_HOST}")
    print("Please see the error below for more details:")
    print(e)
    print("Trying again without any DATABASE_OPTIONS:")
    try:
      psycopg2.connect(
          dbname=DATABASE_NAME,
          user=DATABASE_USER,
          password=DATABASE_PASSWORD,
          host=DATABASE_HOST,
          port=DATABASE_PORT,
      )
    except Exception as e:
      print(f"Error: Failed to connect to the postgresql database at {DATABASE_HOST} without the {DATABASE_OPTIONS}")
      print("Please see the error below for more details:")
      print(e)
      sys.exit(-1)
sys.exit(0)
END
  else
    echo "Checking the provided DATABASE_URL"
    DATABASE_URL=$DATABASE_URL \
      python3 <<END
import sys
import psycopg2
import os
DATABASE_URL=os.getenv('DATABASE_URL')
try:
    psycopg2.connect(
        DATABASE_URL
    )
except psycopg2.OperationalError as e:
    print(f"Error: Failed to connect to the postgresql database at {DATABASE_URL}")
    print("Please see the error below for more details:")
    print(e)
    sys.exit(-1)
sys.exit(0)
END
  fi
}

wait_for_postgres() {
  for i in $(seq 0 "$POSTGRES_STARTUP_CHECK_ATTEMPTS"); do
    if ! postgres_ready; then
      echo "Waiting for PostgreSQL to become available attempt " \
        "$i/$POSTGRES_STARTUP_CHECK_ATTEMPTS ..."
      sleep 2
    else
      echo 'PostgreSQL is available'
      return 0
    fi
  done
  echo 'PostgreSQL did not become available in time...'
  exit 1
}

run_setup_commands_if_configured() {
  if [ "$MIGRATE_ON_STARTUP" = "true" ]; then
    python $APP_HOME/manage.py migrate
  fi

  python $APP_HOME/manage.py collectstatic --noinput
}

if [[ -z "${1:-}" ]]; then
  echo "Must provide arguments to docker-entrypoint.sh"
  exit 1
fi

case "$1" in
gunicorn)
  run_setup_commands_if_configured
  exec /usr/local/bin/gunicorn ${GUNICORN_APPLICATION} --config $APP_HOME/gunicorn_config.py
  ;;
celery)
  exec celery --app app worker -E -l INFO -Q ${CELERY_QUEUES} --concurrency ${CELERY_CONCURRENCY}
  ;;
celery-beat)
  exec celery --app app beat -l INFO
  ;;
celery-flower)
  exec celery \
    --app app \
    -b "${CELERY_BROKER_URL}" \
    --persistent=True --db="flower_db" \
    --max_tasks=1000 \
    flower
  ;;

esac
