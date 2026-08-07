test:
  uv run pytest

template-matrix:
  uv run pytest -m template

template-contracts:
  uv run pytest -m "template or template_integration or template_upgrade"

quality:
  uv lock --check
  uv run ruff format --check hooks scripts tests
  uv run ruff check hooks scripts tests
  uv run pytest

refresh-template-locks:
  uv lock
  uv run python scripts/refresh_template_locks.py
  just template-contracts
