# Project Engineering Guide

This is the operating manual for humans and coding agents working on this
project. It records the technical shape of the application and the engineering
preferences chosen for it. Keep it current when those decisions change.

## Rule vocabulary

- **Must**: an invariant. Do not bypass it merely to complete a task faster.
- **Prefer**: the default approach. Choose another approach only when it is
  demonstrably better for this project.
- **Exception**: document the reason and trade-off in `docs/adr/` before
  introducing a lasting deviation from a Must or a major Prefer.

## Project context

This is a Django application foundation, not a generic Python library. It is
designed for a domain-oriented product with a server-owned security boundary,
an optional HTTP API, and an optional HyperDjango server-rendered interface.

**Must**: complete `docs/product.md` before implementing substantial product
behavior. It records the product purpose, primary users, sensitive-data
classification, external systems, and domain glossary. Do not put volatile
tickets, implementation diaries, or secrets in this file.

## Technical shape

- Python 3.14, Django 6, PostgreSQL, Redis, `uv`, Docker Compose, and Uvicorn.
- Django settings have a template-owned foundation and a project-owned
  composition layer. The project composition layer selects applications,
  identity, routes, and product settings; production settings enforce the
  non-negotiable security baseline after that composition.
- `{{ cookiecutter.project_slug }}/platform/` contains template-owned,
  provider-neutral runtime infrastructure: settings support, health/version
  endpoints, admin integration, storage, observability, logging, tasks, and
  management commands. It owns neither a user model nor an auth provider.
- `{{ cookiecutter.project_slug }}/domains/` is product-owned code. Its
  registry is the extension point for installed apps, navigation, routes, and
  API routers. The top-level `identity/` app owns the default local identity
  implementation.
{% if cookiecutter.rendering_mode in ["api", "hybrid"] %}
- Django Ninja provides the `/api/v1/` layer. It is present because this is a
  `{{ cookiecutter.rendering_mode }}` project.
{% endif %}
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}
- HyperDjango provides the SSR interface. Vite, Tailwind CSS v4, TypeScript,
  and Playwright are present because this is a `{{ cookiecutter.rendering_mode
  }}` project.
{% endif %}
{% if cookiecutter.enable_celery == "yes" %}
- Celery is enabled. It uses one default queue and Beat, with Redis as the
  broker/result backend.
{% else %}
- Celery is intentionally disabled. Do not introduce a background-job system
  without an explicit architecture decision.
{% endif %}

**Must**: use HyperDjango for server-rendered interactivity. Do not introduce
Datastar. Do not add a second web framework, task queue, ORM, settings library,
or dependency-injection container unless an ADR establishes a real need.

## Directory map and ownership

| Location | Owns | Do not put here |
| --- | --- | --- |
| `{{ cookiecutter.project_slug }}/platform/` | reusable, provider-neutral runtime infrastructure and framework integration | user models, auth-provider configuration, product workflows, or domain policy |
| `{{ cookiecutter.project_slug }}/settings/project.py` | application selection and project-specific settings composition | template-wide runtime defaults or production safeguards |
| `{{ cookiecutter.project_slug }}/domains/<domain>/` | domain models, operations, policies, queries, API adapters, and domain tests | page-specific formatting or broad utilities |
| `{{ cookiecutter.project_slug }}/identity/` | local user model, Allauth/JWT integration, auth UI behavior, authorization seams, and identity tests | generic platform runtime behavior |
| `{{ cookiecutter.project_slug }}/api/` | API root/router and shared API concerns | business rules or model serialization |
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}
| `hyper/routes/` | HTTP transport, route-local templates, and page bundles | domain decisions or reusable business logic |
| `hyper/view_models/` | template-ready presentation shaping, labels, grouping, and display state | persistence, parsing, side effects, or business policy |
| `hyper/shared/` | reusable UI components, tokens, and small browser controllers | product-specific route UI |
{% endif %}
| `tests/` | black-box and cross-cutting project-contract tests | duplicate copies of domain tests |
| `docs/adr/` | lasting project decisions and intentional exceptions | temporary task notes |

**Must**: keep transport layers thin. Routes, API handlers, management commands,
and Celery tasks parse input, authorize, call a domain operation, and return a
response. They do not implement business decisions themselves.

**Prefer**: direct Django ORM queries and clear model invariants over generic
repository, service, factory, or abstraction layers. Create an abstraction only
when it removes a demonstrated repeated boundary, not speculative complexity.

## Platform, product, and Cruft boundary

- **Must** make product decisions in `identity/`, `domains/`, product routes,
  view models, and `settings/project.py`. This includes selecting or removing
  applications, the user model, authentication provider, authorization model,
  and product settings.
- **Prefer** the documented extension seams instead of changing
  `{{ cookiecutter.project_slug }}/platform/`. This keeps future template
  updates reviewable, but is not a technical restriction: Cruft permits edits
  and will merge or surface them as conflicts during a later update. Ruff also
  checks the entire generated project, not platform code specially.
- **Must** treat a platform change as a deliberate fork. Before a lasting
  change, write an ADR explaining why no extension boundary fits, list the
  forked files, expected Cruft-update conflict, rollback path, and regression
  tests. Decide whether a reusable part should be proposed upstream. Do not
  hide a product-specific platform fork in an unrelated feature change.
- **Must** preserve the generated Cruft skip list for project-owned paths,
  including `identity/`, `domains/`, `settings/project.py`, product routes,
  view models, product `AGENTS.md`, and product ADRs. Skipped paths are
  intentionally owned by the project; template releases document relevant
  manual migrations rather than overwriting them.

## Product development conventions

- **Must** create product capabilities with
  `just new-domain <name>`; it creates the domain package and its test shape.
- **Must** use `domains/<domain>/operations.py` for business use cases. Keep
  operations framework-light: return domain data or raise domain exceptions,
  rather than returning HTTP responses or template context.
- **Prefer** plain, typed module-level functions for domain operations. Use a
  dataclass only for a coherent input/result value or a stateful collaborator;
  do not introduce generic service, manager, repository, or factory classes.
- **Must not** add a function or helper merely to make code look modular. A new
  function needs a named responsibility and a reason it improves ownership,
  reuse, testing, or a non-trivial flow. Inline a one-use trivial expression
  when it is clearer; do not write single-line functions or helpers.
- **Must** keep persistence constraints and model invariants close to
  `models.py`. Use focused query modules when a complex read deserves a name.
- **Prefer** UUID primary keys for new product models unless an external system
  or existing schema requires another identifier.
- **Prefer** stable identifiers, not model instances, request objects, or raw
  user input, at asynchronous and external-system boundaries.
- **Prefer** bounded queries. Avoid request-path unbounded `__in` filters and
  generated `OR` chains; use joins, `Exists`, pagination, subqueries, or an
  explicitly bounded batch instead.
- **Must** preserve historical records and migrations. Add forward-only
  migrations; never edit or delete an applied migration. Use expand, backfill,
  and contract for incompatible changes.
- **Must** state a reversible assumption and continue when a local requirement
  is incomplete. Ask first before choosing or changing product behavior,
  security, data contracts, architecture, external integrations, material cost,
  or irreversible state.

## API conventions

{% if cookiecutter.rendering_mode in ["api", "hybrid"] %}
- **Must** use explicit Pydantic request/response schemas and mapping functions.
  Never expose Django models, querysets, or model-derived fields as a public API
  by accident.
- **Must** keep API errors conformant with RFC 9457: use
  `application/problem+json` and include a meaningful `type`, `title`,
  `status`, `detail`, and `instance`.
- **Must** preserve `X-Request-ID` in API errors and structured logs. It is for
  correlation only; never put user data, tokens, or secrets in it.
- **Must** version externally consumed endpoints under `/api/v1/`. Make
  compatibility and deprecation explicit before changing a public contract.
{% else %}
This project has no API layer. **Exception**: adding one requires an ADR and
the API contract, error, auth, and CORS rules above.
{% endif %}

## SSR, frontend, and design system

{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}
- **Must** create pages with `just new-route <route>`. A complete route bundle
  contains `+page.py`, `index.html`, `entry.ts`, and `entry.head.ts`.
- **Must** keep `+page.py` transport-only: parse a request, authorize, call
  domain operations, build or request a view model, and render a response.
- **Must** put non-trivial presentation shaping in the route-mirrored
  `hyper/view_models/` package. View models are presentation-only.
- **Must** keep raw HTML event attributes such as `onclick` and `onkeydown` out
  of templates. Route interaction belongs in `entry.ts`; reusable behavior
  belongs in a small controller under `hyper/shared/js/alpine/`.
- **Prefer** existing shared components and shared CSS classes before creating
  page-local markup or CSS. See `docs/shared-ui.md` for the UI component
  contract, upload dropzone, searchable select, icons, and filename safety.
- **Must** preserve the design language: semantic tokens, clear content
  hierarchy, accessible focus states, keyboard operation, responsive layouts,
  and explicit loading, empty, validation, and error states. Do not add colour,
  motion, or bespoke component variants without a user-facing purpose.
- **Prefer** small, declarative TypeScript modules. Keep DOM querying scoped to
  a route root and make frontend behavior progressively enhance a useful SSR
  page.
- **Must** use `just dev` for ordinary SSR or hybrid development. It runs
  HyperDjango's `hyper_runserver`, which supervises Django and Vite, assigns a
  free Vite port, and shares it with Django. Use `just vite` only when
  deliberately pairing it with Django's ordinary `runserver`.
- HyperDjango's Request Inspector is enabled only in development, before file
  routes, with page-request recording disabled so its bounded history focuses
  on actions and SSE streams. Its unpinned traces clear on full refresh; pins
  and traces are process-local and disappear on restart. Do not enable it
  outside a reviewed debugging or access-controlled environment. Use stable
  DOM targets and inspect action traces before adding client-side diagnostic
  logging.
- **Must** treat HyperDjango's retry policy as a delivery guarantee: GET
  actions retry by default and must be read-only; POST actions do not retry by
  default. Enable a retryable POST only with a durable idempotency ledger,
  database uniqueness/conditional transition, and downstream idempotency keys.
- **Must** use named `Checkpoint` items only in retryable GET action streams,
  after a completed permission-checked stage. Read them through
  `get_resume_checkpoint(request, allowed=...)` with a stable ordered allow
  list. `Last-Event-ID` and `X-Hyper-Request-ID` are untrusted progress
  metadata, never authorization, tenant, or resource identity.
- **Must** keep `HYPER_SSE_HEARTBEAT_INTERVAL` below the smallest complete-path
  proxy, CDN, server, or ingress idle timeout when adding streamed actions;
  confirm heartbeats are not buffered and test reconnects through the same
  production topology. Do not disable heartbeats unless that keep-alive review
  explicitly permits it.
- **Must** preserve Vite 8 compatibility: use Node.js `^20.19.0` or
  `>=22.12.0`, keep colocated `entry.ts` and `entry.head.ts` files valid, and
  resolve HyperDjango system-check errors rather than silencing them.
{% else %}
This is API-only. Do not add a frontend build or SSR routes without an ADR.
{% endif %}

## Authentication and authorization

- The generated project defaults to a complete top-level `identity/`
  implementation. It owns the user model, Django Allauth configuration, JWT
  endpoints where an API exists, authentication SSR behavior where SSR exists,
  and authorization extension seams. The platform must remain free of these
  product decisions.
- A project may remove or replace local identity. Do so before the first
  migration whenever possible. Replacing a migrated `AUTH_USER_MODEL` is a
  data-migration and deployment change: write an ADR, migration/rollback plan,
  threat model, configuration documentation, and tests first.
- Select identity and related settings in `settings/project.py`; do not mount
  broad provider URLs merely for convenience. Preserve the custom login,
  logout, registration, and password-reset flows while local identity remains
  selected. Registration remains controlled by `ACCOUNT_ALLOW_REGISTRATION`.
- **Must** keep authentication, authorization, and domain permissions explicit
  at transport boundaries and inside operations that can be invoked by more
  than one transport.
- **Must** treat `SITE_ID` as required configuration for sites and Allauth.
- **Exception**: SSO, SCIM, enterprise role models, or social login are
  application-specific layers. Add them deliberately with an ADR, threat model,
  configuration documentation, and tests.
- Admin impersonation is an exception-only support capability. It is disabled
  by `ENABLE_ADMIN_HIJACK` unless deliberately enabled. **Must** preserve the
  superuser-to-active-regular-user policy, visible warning/exit control, and
  immutable start/end audit events. Never impersonate staff or superuser users,
  and never disable the warning banner.

## Rate limiting

- **Must** assess every new externally reachable route or API operation for a
  rate-limit policy before implementation. Public authentication, password
  reset, registration, invitations, verification/OTP, uploads, exports,
  outbound-email triggers, search, expensive reads, and every state-changing
  operation require an explicit limit.
- **Must** use `platform.ratelimits.enforce_rate_limit` or
  `enforce_public_auth_rate_limits`; do not add view-local, in-memory, or
  database-counter implementations. Reuse the broad API IP policy and add a
  narrower operation policy where risk warrants it.
- **Must** attach `APIIPRateThrottle()` when registering every Django Ninja
  router. Ninja does not inherit an API-level throttle into routers added later;
  use `api.add_router(..., throttle=APIIPRateThrottle())`, then add an
  operation-specific policy for sensitive routes.
- **Must** use independent trusted-IP and normalized-account/user/API-key
  counters for publicly reachable credential or account actions. A single IP
  limit is insufficient against distributed attacks; a single account limit is
  insufficient against a single host spraying accounts.
- **Must** return RFC 9457 `429` API responses and a `Retry-After` header.
  Keep responses non-enumerating: never reveal whether an email, account,
  invite, reset token, or credential exists.
- **Must** keep rates configurable through the documented environment settings,
  enabled by default, and use Redis-backed atomic counters. Do not fail open
  when the rate-limit cache is unavailable.
- **Must** treat application limits as a second layer. Configure ingress/WAF
  rate and request-size limits too, and set `UVICORN_FORWARDED_ALLOW_IPS` only
  to proxy networks that remove client-supplied forwarding headers. Never use
  `*` for a publicly reachable application without an explicit, reviewed trust
  boundary.

## Email

- **Must** send application email through `platform.emails` using MRML-rendered
  MJML. The template intentionally does not ship an email layout or example
  message.
- When the product needs branded application email, **must** create the
  product-owned `templates/email/base.mjml` first. Use it as the shared layout
  for that product's child email templates, which should contain only
  use-case-specific content and voice.
- **Must not** build HTML in Python, duplicate a product email layout, or send
  HTML-only email; the shared sender supplies a text alternative.

## Configuration, security, and data handling

- **Must** read configuration through
  `{{ cookiecutter.project_slug }}.config.env`; do not access `os.environ`
  outside settings/bootstrap code.
- **Must** document every runtime setting in `docs/configuration.md` and cover
  it with the configuration-contract tests. Do not introduce undocumented
  environment variables or silently retire one; mark deprecations explicitly.
- **Must** keep secrets out of Git, logs, exceptions, fixtures, screenshots,
  test names, documentation, request IDs, and client responses. Never log
  request bodies, credentials, bearer tokens, passwords, cookies, or session
  data.
- **Must** preserve production fail-closed behavior: real `SECRET_KEY`, allowed
  hosts, TLS, secure cookies, origin-specific CORS, CSP without `unsafe-inline`
  or `unsafe-eval`, logging redaction, and RFC 9457 API errors where present.
- **Must** put project-specific configuration and application selection in
  `settings/project.py`. Production enforcement is applied after that layer;
  do not weaken it through a routine settings override. A genuine exception is
  a platform fork and requires the ADR, rollback, and regression-test record
  described above.
- **Must** keep static assets public and media private/signed by default when
  using S3. Do not turn a media bucket public to simplify a feature.
- **Prefer** explicit retention, deletion, audit, and data-classification
  decisions before storing user or regulated data. Record those decisions in an
  ADR or linked product documentation.
- Sentry and OpenTelemetry integrations are opt-in through configuration;
  preserve redaction and correlation before enabling new telemetry.

## Observability

- **Must** treat telemetry as a product contract. Before adding a log event,
  span, or metric, define the operator question it answers; for product metrics,
  also define the owner, dashboard, alert threshold, and runbook in the same
  change.
- **Must** use static dotted event names and structured fields for logs. Keep
  `request_id`, and active `trace_id`/`span_id`, intact. Never log request or
  response bodies, headers, query strings, credentials, cookies, tokens,
  email contents, unredacted provider payloads, or regulated data. Platform
  redaction is defence in depth, not permission to emit unsafe values.
- **Must** use OpenTelemetry as the sole performance-tracing owner. Preserve
  parent-based sampling, trace the template-provided HTTP and Celery boundaries
  only, and keep Sentry focused on redacted errors. Do not enable Sentry
  performance tracing, database tracing, Redis tracing, or arbitrary span
  attributes without an ADR covering privacy, retention, cost, and cardinality.
- **Must** use metric names and labels with finite, reviewed values. Route
  patterns are allowed; raw paths, URLs, query values, IDs, emails, task IDs,
  exception messages, and external identifiers are forbidden as labels. Add
  product metrics beside the owning domain operation, not in `platform/`.
- **Must** keep `/metrics/` disabled unless a private monitoring path and
  `METRICS_TOKEN` secret are configured. Scrapers send the token in an
  `Authorization: Bearer` header; never put it in a URL, log it, or expose the
  endpoint through public ingress. Run one Uvicorn worker per container when
  scraping the in-process registry unless a reviewed multiprocess aggregation
  strategy exists.
- Read `docs/observability.md` before adding or changing telemetry.

## Background work

{% if cookiecutter.enable_celery == "yes" %}
- **Must** make Celery tasks thin adapters over idempotent domain operations.
  They inherit `DomainTask` so correlation, late acknowledgement, bounded
  retries, and time limits remain consistent.
- **Must** treat delivery as at-least-once: a task may run more than once after
  a worker loss. Never claim exactly-once, always-once, or almost-once
  delivery. Build effectively-once business outcomes with an idempotency key,
  database uniqueness/conditional state transitions, transactional outbox or
  inbox where a boundary is crossed, and external-provider idempotency keys.
- **Must** define retries, terminal failures, timeouts, idempotency, external
  side effects, and recovery before enqueueing work. Retry only bounded,
  proven transient failures; never blindly retry validation, authorization, or
  permanent provider errors. At-most-once is allowed only for explicitly
  disposable work whose acceptable loss is documented.
- **Must** send stable, small primitive task arguments; never requests, model
  instances, secrets, or unbounded input. Do not keep a database transaction
  open over network I/O. Use explicit claim/state transitions for concurrent
  work and document dedicated queues before introducing long-running jobs.
- **Prefer** synchronous domain operations for ordinary request work. Avoid
  `async_to_sync` and `sync_to_async`; obtain explicit approval before adding
  them as a practical necessity.
{% endif %}

## Commands and verification

| Intent | Command |
| --- | --- |
| First local setup | `just setup` |
| Start PostgreSQL and Redis | `just services-up` |
| Diagnose environment safely | `just doctor` |
| Run the development server | `just dev` |
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}
| Run Vite development assets | `just vite` |
| Build frontend assets | `just build-assets` |
| Run browser E2E | `just e2e` |
{% endif %}
| Create migrations | `just makemigrations` |
| Apply migrations | `just migrate` |
| Run focused test | `just test-one <path-or-nodeid>` |
| Run authoritative verification | `just verify` |
| Verify production settings | `just production-check` |
| Inspect template update state | `just cruft-check` |

- **Must** add or update tests with every executable behavior change.
- **Must** maintain 100% branch coverage for project-owned executable code. Do
  not weaken coverage exclusions or lower the threshold to make a change pass.
- **Must** run `just verify` before handoff. It is the trusted local and CI
  command for locks, format, lint, type checks, security, migrations,
  production settings, frontend checks when present, and tests.
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}
- **Must** also run `just e2e` for browser, SSR, or authentication-flow changes.
{% endif %}
- **Must** keep Ruff, djLint, basedpyright, Bandit, Prettier, Gitleaks, pytest,
  and Playwright as the relevant sources of truth. Do not add overlapping
  linting or test tooling without an ADR.

## Dependencies, template updates, and release provenance

- **Must** make dependency changes intentionally. Update `pyproject.toml`,
  regenerate the committed `uv.lock`, explain the reason, and rerun
  `just verify`; do not hand-edit a lockfile.
- This project was created with Cruft. **Must** run `cruft check`, commit or
  stash product work, review the update diff, and resolve conflicts deliberately
  before `cruft update`. Re-run `cruft check` afterwards.
- **Must** keep product code under the documented extension boundaries so
  template updates remain reviewable. Do not modify template-owned platform
  code for a product feature when a domain extension is appropriate.
- SBOM attachment and image provenance are optional release layers. See
  `docs/release-provenance.md`; do not make them a local-developer burden.

## Change workflow and living context

1. Read `docs/product.md` and the relevant architecture, security,
   configuration, and domain context before changing behavior. For
   cross-cutting or lasting decisions, create an ADR first.
2. Make the smallest coherent change in the correct ownership boundary.
3. Update tests, docs, configuration contracts, and generated UI/API artifacts
   together with behavior.
4. Run the required verification and report what passed, what was intentionally
   skipped, and any follow-up risk.
5. Update this file when a technical rule, tool, architectural boundary, or
   preference changes.

**Prefer** a nested `AGENTS.md` inside a mature domain or integration when it
has rules that would otherwise make this root guide noisy. The nested guide
should state only the local vocabulary, data contracts, invariants, and test
commands; it overrides this guide for its subtree.
