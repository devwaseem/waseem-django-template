# Agent Guide

## Core rules

- Keep routes, API handlers, management commands, and Celery tasks thin. Celery tasks should inherit `DomainTask` so retry and correlation behavior remains consistent. Put
  business use cases in `domains/<domain>/operations.py`.
- Keep persistence and model invariants in `models.py`; use direct ORM/query
  modules where clarity needs them. Do not add generic repository or service
  abstractions.
- API contracts use explicit Pydantic schemas and mapping functions. Never
  expose Django models as public API responses.
- Put non-trivial SSR presentation shaping in the route-mirrored
  `hyper/view_models/` package. Keep it presentation-only.
- Use `just new-domain <name>` for a new domain and, for SSR-capable projects,
  `just new-route <route>` for a new page bundle. Do not hand-create a partial
  route.

## Configuration and security

- Read configuration only through `{{ cookiecutter.project_slug }}.config.env`.
  Do not access `os.environ` outside settings/bootstrap modules.
- Preserve `X-Request-ID` through logs, task handoff, and API problem responses; do not put user data in it.
- Keep secrets out of Git, logs, exceptions, tests, screenshots, fixtures, and
  documentation. Never log request bodies, bearer tokens, cookies, passwords,
  or credentials.
- Preserve the private-signed-media and public-static-storage split when
  extending S3 support.
- Keep API CORS opt-in and origin-specific. Do not enable wildcard origins.
- Preserve CSP without `unsafe-inline` or `unsafe-eval`; use a nonce only when
  a genuinely necessary inline script is added.

## Quality

- Add tests with every executable change and maintain 100% branch coverage for
  project-owned code. Do not dilute coverage exclusions.
- Run `just verify` before handoff; run `just e2e` as well for SSR-capable UI/auth changes.
- Migrations are forward-only. Never edit or delete an applied migration; use
  expand, backfill, contract for incompatible changes.
- Keep Ruff, djLint, basedpyright, Bandit, Prettier, Gitleaks, pytest, and
  Playwright as the single sources of truth. Do not add overlapping linters.

## Template update boundary

- This project was created with Cruft. Use `cruft check` before and after an
  update, review the diff, and resolve merge conflicts deliberately.
- Treat platform code, extension registries, and documented extension points as
  template-owned. Keep product-specific behavior under `domains/` and
  product-specific UI under routes/view models so Cruft updates remain safe.
- Record product-specific architecture decisions as ADRs under `docs/adr/`, not
  in this file. These instructions apply to humans and AI agents alike.
