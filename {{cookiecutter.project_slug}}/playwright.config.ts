import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "tests/e2e",
  fullyParallel: true,
  use: {
    baseURL: "http://127.0.0.1:8000",
    trace: "retain-on-failure",
  },
  webServer: {
    command: "uv run --env-file .env python manage.py runserver 127.0.0.1:8000",
    port: 8000,
    reuseExistingServer: !process.env.CI,
  },
});
