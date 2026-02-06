# Observability

## Health Endpoints
When `ENABLE_HEALTH_CHECK=true`:
- `/healthz/` runs full health checks
- `/readyz/` runs readiness checks (db/cache/redis)

## Structured Logging
Request logging is enabled via `django-structlog`. Use your log shipper to
capture JSON logs and correlate with request IDs.

## Sentry
Set `ENABLE_SENTRY=true` and `SENTRY_DSN` to enable Sentry in production.
