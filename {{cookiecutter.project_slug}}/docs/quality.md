# Quality

`just verify` is the authoritative generated-project check for developers and CI: it validates locks, formatting, linting, types, security, migration state, production configuration, frontend formatting and builds when present, and the 100% coverage suite. It explicitly reports API-only frontend and disabled-Celery checks as skipped. Browser E2E remains an intentional follow-up for SSR/hybrid browser or auth-flow changes.

`just doctor` performs a read-only tool, lockfile, Compose, PostgreSQL, Redis, and rendering-mode diagnosis. `just production-check` proves production settings fail closed and passes Django's deploy checks; it is included in `just verify` for local pre-push and generated-project CI.

`just quality` runs the lockfile check, formatting, Ruff, djLint, strict
basedpyright, Bandit, and pre-commit hooks. `just test` enforces 100% branch
coverage for project-owned executable code. Framework dependencies, migrations,
settings, and bootstrap entrypoints are excluded deliberately.

The normal pre-commit hook is fast. Pre-push and the primary GitHub Actions job run `just verify`; GitHub Actions additionally runs browser checks before changes reach `main`.
