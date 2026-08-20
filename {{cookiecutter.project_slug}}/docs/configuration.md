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
| `DEPLOYMENT_ENVIRONMENT` | Deployment name applied to error reports and traces. | `development`; use a stable value such as `staging` or `production`. |
| `SITE_ID` | django-allauth site selection. | `1`. |
| `ACCOUNT_ALLOW_REGISTRATION` | Enables public account creation. | `true`; application-specific after generation. |
| `ENABLE_ADMIN_HIJACK` | Enables auditable Django-admin impersonation. | `false`; enable only under an approved support-access policy. |
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}
| `HYPER_VITE_DEV_SERVER_URL` | Vite URL used only by Django's ordinary `runserver`. | `http://localhost:5173/`; `just dev` supplies a selected URL automatically. |
| `HYPER_SSE_HEARTBEAT_INTERVAL` | Idle seconds between HyperDjango SSE heartbeat comments. | `15`; use `0` only when the complete production path does not need stream keep-alives. |
{% endif %}

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
| `RATELIMIT_ENABLE` | Enables application-level request rate limits. | `true`; disable only in an isolated local test. |
| `RATE_LIMIT_API_IP` | Broad API requests allowed per trusted client IP. | `120/m`. |
| `RATE_LIMIT_LOGIN_IP` | Login attempts allowed per trusted client IP. | `5/15m`. |
| `RATE_LIMIT_LOGIN_ACCOUNT` | Login attempts allowed per normalized account identifier. | `5/15m`. |
| `RATE_LIMIT_REGISTRATION_IP` | Registration attempts allowed per trusted client IP. | `3/h`. |
| `RATE_LIMIT_REGISTRATION_ACCOUNT` | Registration attempts allowed per normalized account identifier. | `5/d`. |
| `RATE_LIMIT_PASSWORD_RESET_IP` | Password-reset requests allowed per trusted client IP. | `3/h`. |
| `RATE_LIMIT_PASSWORD_RESET_ACCOUNT` | Password-reset requests allowed per normalized account identifier. | `3/h`. |
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

{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}
## HyperDjango development

`just dev` runs HyperDjango's `hyper_runserver`, which supervises Django and
the project-local Vite server in one process group. It chooses a free Vite port
and temporarily supplies `HYPER_VITE_DEV_SERVER_URL`; do not pin the variable
unless deliberately using Django's ordinary `runserver` with `just vite`.

Development enables HyperDjango's process-local Request Inspector with a
50-request history at `/__hyperdebug__/`. It records Hyper actions and streams,
but not ordinary page loads (`RECORD_PAGE_REQUESTS=False`), keeping the tape
focused on dynamic behavior. It is development-only: do not enable its app,
middleware, URLs, or `HYPER_DEBUG_TOOLBAR` in a public environment without an
explicit access and data-retention decision. Its unpinned traces clear on a
full browser refresh; pinned traces survive the refresh and history eviction,
but every trace and pin remains process-local and disappears on restart. The
development logging configuration suppresses only the Inspector's own access
logs, leaving ordinary page and action access logs intact.

## HyperDjango streams

HyperDjango emits a transport-only `: heartbeat` comment after the configured
idle interval for generator action streams. Set
`HYPER_SSE_HEARTBEAT_INTERVAL` below the smallest proxy/CDN/server idle timeout
and verify the comment is not buffered. A `GET` action retries by default;
`POST` does not. A product may explicitly retry a POST only after it has an
idempotency ledger and downstream idempotency keys.

For a retryable GET stream, yield named `Checkpoint` items only after a
completed, authorization-checked stage and use `get_resume_checkpoint()` with
a stable allowed list to skip it on reconnect. `Last-Event-ID` and
`X-Hyper-Request-ID` are untrusted progress metadata, never authorization or
tenant identifiers. Checkpoint names and their ordering are a deployment
contract; test reconnects through the real proxy path.
{% endif %}

When `ENABLE_ADMIN_HIJACK` is true, `HIJACK_PERMISSION_CHECK` still allows only
active superusers to impersonate active non-staff, non-superuser accounts.
`HIJACK_INSERT_BEFORE` keeps a visible stop-impersonating warning in every
response, and the generated `platform.AdminImpersonationAuditEvent` stores the
start/end actor, target, timestamp, direct remote address, and request ID.
These settings are code-owned safety controls, not environment switches.

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

## Rate limiting

The application uses the default Redis cache for atomic rate-limit counters;
`RATELIMIT_USE_CACHE` is code-owned and remains `default`.
Limits apply independently by trusted client IP and, for public authentication
flows, by normalized account identifier. A blocked API response is an RFC 9457
`429` problem response with `Retry-After`; a blocked HTML request uses the
shared 429 page and the same header.

Application limits are a fairness and brute-force control, not DDoS protection.
Production must also enforce a coarse IP limit and request-size policy at its
ingress or WAF. `RATELIMIT_FAIL_OPEN` is code-owned and false: Redis failures
block protected application traffic rather than silently removing protection.

## Observability and server

| Variable | Runtime use | Default / requirement |
| --- | --- | --- |
| `SENTRY_DSN` | Enables redacted Sentry error reporting. | Empty disables it; Sentry performance tracing remains off because OpenTelemetry owns traces. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Enables OTLP trace export. | Empty disables it. Use the trace collector HTTP/protobuf endpoint, usually ending in `/v1/traces`. |
| `OTEL_SERVICE_NAME` | OpenTelemetry and Sentry release service name. | Project slug. |
| `OTEL_TRACE_SAMPLE_RATIO` | Parent-based OpenTelemetry head-sampling probability. | `0.1`; must be between `0` and `1`. |
| `METRICS_ENABLED` | Enables the private Prometheus `/metrics/` scrape route and HTTP metrics. | `false`. |
| `METRICS_TOKEN` | Bearer token required by the Prometheus scrape route. | Empty while metrics are disabled; required if enabled in production. |
| `UVICORN_HOST` | Uvicorn listen host. | `0.0.0.0`. |
| `UVICORN_PORT` | Uvicorn listen port. | `8000`. |
| `UVICORN_WORKERS` | Uvicorn worker count. | `1`. |
| `UVICORN_TIMEOUT_KEEP_ALIVE` | Uvicorn keep-alive timeout in seconds. | `5`. |
| `UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN` | Graceful shutdown timeout in seconds. | `30`. |
| `UVICORN_FORWARDED_ALLOW_IPS` | Comma-separated proxy IPs or networks allowed to supply forwarded client details. | `127.0.0.1`; set to the actual ingress network in production. |

Uvicorn accepts forwarded client headers only from
`UVICORN_FORWARDED_ALLOW_IPS`. Do not use `*` unless the application is
network-isolated behind a proxy that removes every client-supplied forwarded
header before adding its own.

See [Observability](observability.md) for the metric inventory, scrape
security, trace sampling, and the required dashboard/alert decisions.

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
