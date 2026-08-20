# Security

Production fails closed without a real secret, allowed hosts, and TLS. The
default password hasher is Argon2. Cookies use secure and same-site settings
when TLS is enabled; CORS is disabled until explicit origins are configured.

Media S3 storage is private and signed by default. Static assets are public
through a bucket policy or CDN and do not receive signed URLs.

Logs and telemetry must not contain credentials, bearer tokens, cookies,
passwords, request bodies, headers, query strings, or secret-bearing cache
keys. Sentry error reporting and OpenTelemetry trace export remain inactive
until their environment configuration is provided. Prometheus metrics stay
disabled until a private scraper and bearer token are configured; never expose
`/metrics/` through a public ingress. See [Observability](observability.md).

## Request rate limits

Redis-backed application limits are enabled by default. They apply a broad API
IP policy and stricter, independent IP and normalized-account policies to
login, registration, and password-reset requests. Application code must use
the shared rate-limit policy for new public or expensive operations; do not add
ad-hoc in-memory counters or silently disable limits outside an isolated test.

`429` responses never disclose whether an account exists and include a
`Retry-After` header. Application limits are not a DDoS boundary: production
must also configure a coarse rate and request-size limit at its ingress or WAF.
Uvicorn trusts forwarded client details only from the explicitly configured
`UVICORN_FORWARDED_ALLOW_IPS` proxy network. Never trust forwarded headers from
the public internet.

## Privileged support access

Django-admin impersonation is disabled by default through
`ENABLE_ADMIN_HIJACK=false`. When explicitly enabled, only an active superuser
can impersonate an active account that is neither staff nor a superuser. The
UI must retain its visible warning and exit control. Every successful start and
end is stored as an append-only audit event with actor, target, time, direct
remote address, and request correlation ID. Do not trust `X-Forwarded-For` in
application code; configure a trusted ingress separately if the real client IP
must be retained.
