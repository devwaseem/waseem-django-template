import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "tests/e2e",
  fullyParallel: true,
  use: {
    baseURL: "http://127.0.0.1:8001",
    trace: "retain-on-failure",
  },
  webServer: {
    command:
      "env DJANGO_SETTINGS_MODULE={{ cookiecutter.project_slug }}.settings.test uv run --env-file .env python manage.py runserver 127.0.0.1:8001 --insecure",
    port: 8001,
    reuseExistingServer: false,
  },
});
