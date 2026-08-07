# Cruft workflow

Create a project with:

```bash
cruft create /path/to/waseem-django-template
```

Cruft records the source template and answers in `.cruft.json`. Before updating,
commit or stash product changes, run `cruft check`, then run `cruft update` and
resolve conflicts at the documented extension boundaries. The template repository tests this update path with a product-owned domain extension; keep product code in those boundaries so that contract remains true. Cookiecutter remains
supported for teams that do not need updates:

```bash
cookiecutter /path/to/waseem-django-template
```
