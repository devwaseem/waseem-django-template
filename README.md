# waseem-django-template

A Cruft-first Cookiecutter for a secure Django 6 project that can generate an
API, a HyperDjango SSR application, or both. It carries reusable engineering
patterns—not product-domain behavior—from SmoothPay.

## Create a project

```bash
cruft create /path/to/waseem-django-template
# or
cookiecutter /path/to/waseem-django-template
```

The six prompts are project name, Python-safe slug, presentation timezone,
license, rendering mode, and Celery. Infrastructure and security behavior are
environment configuration, not generation choices.

## Maintain the template

```bash
uv sync
uv run pytest -m template
```

The local pre-push hook renders all six supported rendering/Celery combinations.
Generated projects run their own test, coverage, quality, and (where applicable)
browser checks in GitHub Actions.

## Refresh template lockfiles

Generated projects receive one committed `uv.lock` for their selected shape.
The template retains six parameterized internal variants so the generated
project's own package name is recorded correctly without resolving dependencies
during project creation. After an intentional dependency update, regenerate the
template lock and all generated-project variants with:

```bash
just refresh-template-locks
```
