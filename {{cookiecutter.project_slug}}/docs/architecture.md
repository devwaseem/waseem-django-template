# Architecture

`{{ cookiecutter.project_slug }}` contains template-owned platform code:
settings, user/auth infrastructure, observability, storage, and extension
registries. `domains/` contains product code. Routes and API handlers adapt
HTTP to domain operations; they do not own business decisions.

`domains/registry.py` is the stable extension point for installed domain apps,
routes, API routers, and dashboard navigation. Keep template boundaries narrow
to make Cruft updates predictable.

{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}
HyperDjango provides SSR page bundles. A route has `+page.py`, `index.html`,
`entry.ts`, and `entry.head.ts`; use `just new-route` so each stays complete.
{% endif %}

{% if cookiecutter.enable_celery == "yes" %}
Celery uses one default queue and Beat. Tasks are thin idempotent adapters that
call domain operations; task arguments should be stable identifiers, not model
instances or request objects. Delivery is at-least-once: a worker crash can
redeliver a late-acknowledged task. Make business outcomes effectively once with
database uniqueness, idempotency keys, transactional outbox/inbox boundaries,
and provider idempotency keys. See `background-work.md`.
{% endif -%}

Application email is rendered with MRML from product-owned MJML templates.
When a product adopts email, it creates `templates/email/base.mjml` and sends
through `platform.emails`, which supplies both HTML and a plain-text fallback.
