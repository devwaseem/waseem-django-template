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
