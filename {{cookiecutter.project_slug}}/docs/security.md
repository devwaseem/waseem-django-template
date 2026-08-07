# Security

Production fails closed without a real secret, allowed hosts, and TLS. The
default password hasher is Argon2. Cookies use secure and same-site settings
when TLS is enabled; CORS is disabled until explicit origins are configured.

Media S3 storage is private and signed by default. Static assets are public
through a bucket policy or CDN and do not receive signed URLs.

Logs and telemetry must not contain credentials, bearer tokens, cookies,
passwords, or request bodies. Sentry and OTEL wiring is present but remains
inactive until its environment configuration is provided.
