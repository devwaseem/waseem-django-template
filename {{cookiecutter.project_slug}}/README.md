# {{ cookiecutter.project_name }}

{{ cookiecutter.rendering_mode|capitalize }} Django project generated with
[`waseem-django-template`](../README.md), with {{ "Celery enabled" if cookiecutter.enable_celery == "yes" else "no Celery worker" }}.

## Start locally

```bash
just setup          # creates .env only when it does not exist
just services-up
just migrate
just dev
```

{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}
In a second terminal, run `just vite` for frontend development.
{% endif %}

The app is available at `http://localhost:8000`; the Django admin is at
`/admin/`. API variants expose the OpenAPI docs at `/api/v1/docs`.

## Everyday checks

```bash
just doctor
just verify
# Individual checks remain available: just test, just quality, just migrations-check, just production-check
{% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}just e2e
{% endif %}
```

Read the [documentation](docs/index.md) before extending the project. In
particular, follow the Cruft update boundary in [AGENTS.md](AGENTS.md).
