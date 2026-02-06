# Settings

## Modules
- Development: `app.settings.dev`
- Production: `app.settings.prod`
- Test: `app.settings.test`

## Required Production Values
Set these before deployment:
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `USE_SSL=true`

## Runtime Protections
Production defaults are controlled via:
- `SECURE_REFERRER_POLICY`
- `SECURE_CROSS_ORIGIN_OPENER_POLICY`
- `SECURE_CROSS_ORIGIN_EMBEDDER_POLICY`
- `SECURE_CROSS_ORIGIN_RESOURCE_POLICY`

## CSP
The project uses Django’s built-in CSP with nonces in production and a relaxed
policy in development for Vite.
