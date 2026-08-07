# Security

Production fails closed without a real secret, allowed hosts, and TLS. The
default password hasher is Argon2. Cookies use secure and same-site settings
when TLS is enabled; CORS is disabled until explicit origins are configured.

Media S3 storage is private and signed by default. Static assets are public
through a bucket policy or CDN and do not receive signed URLs.

Logs and telemetry must not contain credentials, bearer tokens, cookies,
passwords, or request bodies. Sentry and OTEL wiring is present but remains
inactive until its environment configuration is provided.

## Privileged support access

Django-admin impersonation is disabled by default through
`ENABLE_ADMIN_HIJACK=false`. When explicitly enabled, only an active superuser
can impersonate an active account that is neither staff nor a superuser. The
UI must retain its visible warning and exit control. Every successful start and
end is stored as an append-only audit event with actor, target, time, direct
remote address, and request correlation ID. Do not trust `X-Forwarded-For` in
application code; configure a trusted ingress separately if the real client IP
must be retained.
