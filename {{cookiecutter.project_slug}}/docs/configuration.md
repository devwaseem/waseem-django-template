# Configuration contract

`.env.example` and this page are the generated project's configuration
contract. Every listed variable is consumed by the runtime, Compose, or a
bootstrap entrypoint. Add a variable to both places in the same change; do not
read the environment directly from application code.

## Application and account settings

| Variable | Runtime use | Default / requirement |
| --- | --- | --- |
| `DJANGO_SETTINGS_MODULE` | Selects the Django settings module. | `{{ cookiecutter.project_slug }}.settings.dev` locally. |
| `DEBUG` | Enables local development behavior. | `true` locally; always `false` in production. |
| `SECRET_KEY` | Django cryptographic signing. | Required; replace the development value before deployment. |
| `ALLOWED_HOSTS` | Allowed HTTP hostnames. | Required in production. |
| `APP_VERSION` | `/version/` release version. | `0.1.0`. |
| `APP_BUILD_SHA` | `/version/` build identifier. | `development`. |
| `SITE_ID` | django-allauth site selection. | `1`. |
| `ACCOUNT_ALLOW_REGISTRATION` | Enables public account creation. | `true`; application-specific after generation. |

## Database, cache, and email

| Variable | Runtime use | Default / requirement |
| --- | --- | --- |
| `POSTGRES_DB` | PostgreSQL database name. | Required. |
| `POSTGRES_USER` | PostgreSQL user. | Required. |
| `POSTGRES_PASSWORD` | PostgreSQL password. | Required and secret. |
| `POSTGRES_HOST` | PostgreSQL host. | Required. |
| `POSTGRES_PORT` | PostgreSQL port. | `5432`. |
| `POSTGRES_HOST_PORT` | Host port published by Compose. | `5432`; Compose-only. |
| `CONN_MAX_AGE` | Django database connection reuse. | `0` locally. |
| `DB_CONNECT_TIMEOUT` | PostgreSQL connection timeout in seconds. | `10`. |
| `REDIS_URL` | Cache and Redis integration endpoint. | Required. |
| `REDIS_HOST_PORT` | Host port published by Compose. | `6379`; Compose-only. |
| `EMAIL_BACKEND` | Django email backend. | SMTP backend; console backend locally. |
| `EMAIL_HOST` | SMTP host. | `localhost`. |
| `EMAIL_PORT` | SMTP port. | `1025`. |
| `EMAIL_HOST_USER` | SMTP user. | Empty. |
| `EMAIL_HOST_PASSWORD` | SMTP password. | Empty; secret when set. |
| `EMAIL_USE_TLS` | Enables SMTP TLS. | `false`. |
| `DEFAULT_FROM_EMAIL` | Application sender address. | `no-reply@example.test`. |
| `SERVER_EMAIL` | Django error sender address. | `system@example.test`. |

## Transport and API security

| Variable | Runtime use | Default / requirement |
| --- | --- | --- |
| `USE_SSL` | Enables HTTPS redirects and secure cookies. | `false` locally; required in production. |
| `SECURE_HSTS_SECONDS` | HSTS duration in production. | `31536000`. |
| `CSRF_TRUSTED_ORIGINS` | Explicit cross-origin CSRF origins. | Empty. |
| `CORS_ALLOWED_ORIGINS` | Explicit cross-origin API origins. | Empty; never use `*`. |

`CONTENT_SECURITY_POLICY` restricts scripts and styles to self (with a script
nonce), and forbids frames, plugins, and unrestricted form targets.
`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, and `CORS_ALLOW_ALL_ORIGINS`
are controlled by `USE_SSL` and the production settings; wildcard CORS is
rejected. `LOGGING` always applies credential redaction before events reach an
output sink.

## Storage

| Variable | Runtime use | Default / requirement |
| --- | --- | --- |
| `STATIC_USE_S3` | Enables S3-backed public static assets. | `false`. |
| `MEDIA_USE_S3` | Enables S3-backed private media uploads. | `false`. |
| `AWS_ACCESS_KEY_ID` | S3 access key. | Required when either S3 switch is enabled. |
| `AWS_SECRET_ACCESS_KEY` | S3 secret key. | Required and secret when either S3 switch is enabled. |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket name. | Required when either S3 switch is enabled. |
| `AWS_S3_REGION_NAME` | S3 region. | Required when either S3 switch is enabled. |

`STORAGES` uses `PrivateMediaStorage` for signed, private uploads and
`PublicStaticStorage` for public static assets. Keep their bucket prefixes
separate.

## Observability and server

| Variable | Runtime use | Default / requirement |
| --- | --- | --- |
| `SENTRY_DSN` | Enables Sentry error reporting. | Empty disables it. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Enables OTLP export. | Empty disables it. |
| `OTEL_SERVICE_NAME` | OpenTelemetry service name. | Project slug. |
| `UVICORN_HOST` | Uvicorn listen host. | `0.0.0.0`. |
| `UVICORN_PORT` | Uvicorn listen port. | `8000`. |
| `UVICORN_WORKERS` | Uvicorn worker count. | `1`. |
| `UVICORN_TIMEOUT_KEEP_ALIVE` | Uvicorn keep-alive timeout in seconds. | `5`. |
| `UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN` | Graceful shutdown timeout in seconds. | `30`. |

{% if cookiecutter.enable_celery == "yes" %}
## Celery

| Variable | Runtime use | Default / requirement |
| --- | --- | --- |
| `CELERY_BROKER_URL` | Celery broker endpoint. | Redis database `1` locally. |
| `CELERY_RESULT_BACKEND` | Celery result backend. | Redis database `2` locally. |
{% endif %}

## Deprecated environment variables

None. To deprecate a variable, retain it in this section with its replacement
and removal version until no generated runtime consumes it.
