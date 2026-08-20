import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

test("registration is accessible and creates a session", async ({ page }) => {
  const runtimeResponse = page.waitForResponse(
    (response) => new URL(response.url()).pathname === "/static/hyperdjango/hyper.js",
  );
  await page.goto("/register/");
  expect((await runtimeResponse).status()).toBe(200);
  await expect(page.getByRole("heading")).toBeVisible();
  await expect(new AxeBuilder({ page }).analyze()).resolves.toMatchObject({ violations: [] });

  await page.getByLabel(/email/i).fill("e2e@example.test");
  await page.locator('input[name="password1"]').fill("Correct-horse-battery-1");
  await page.locator('input[name="password2"]').fill("Correct-horse-battery-1");
  await page.getByRole("button", { name: /create account|sign up|register/i }).click();
  await expect(page).toHaveURL(/\/$/);
});
