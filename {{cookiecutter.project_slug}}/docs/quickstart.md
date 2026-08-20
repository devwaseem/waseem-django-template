# Quickstart

1. Run `just setup`; it copies `.env.example` only when `.env` does not exist.
2. Run `just services-up` to start PostgreSQL and Redis.
3. Run `just migrate`, then `just dev`.
4. {% if cookiecutter.rendering_mode in ["ssr", "hybrid"] %}`just dev` starts Django and Vite together. Open the Request Inspector from any page with <kbd>Control</kbd> + <kbd>Shift</kbd> + <kbd>H</kbd>.{% else %}Open `/api/v1/docs` to explore the contract.{% endif %}

Use the presentation timezone chosen at generation time for user-facing dates;
all persisted datetimes remain UTC.
