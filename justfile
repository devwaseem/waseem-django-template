test:
  uv run pytest

template-matrix:
  uv run pytest -m template

template-contracts:
  uv run pytest -m "template or template_integration or template_upgrade"

quality:
  uv run ruff format --check hooks tests
  uv run ruff check hooks tests
  uv run pytest
