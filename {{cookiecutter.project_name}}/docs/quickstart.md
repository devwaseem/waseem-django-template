# Quickstart

## 1) Configure Environment
```bash
cp env_template.txt .env
```

## 2) Install Dependencies
```bash
uv sync --dev
npm install
```

## 3) Run Django
```bash
direnv allow
uv run python manage.py runserver
```

`.envrc` watches `.env` and loads env vars automatically via direnv.
If direnv is unavailable, use `uv run --env-file .env ...` for commands.

## 4) Run Vite
```bash
npm run dev
```

## Common Commands
- `just dev`
- `just vite`
- `just test`
- `just lint`
