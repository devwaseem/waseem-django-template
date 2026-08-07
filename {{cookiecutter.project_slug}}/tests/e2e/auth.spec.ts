import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

test("registration is accessible and creates a session", async ({ page }) => {
  await page.goto("/register/");
  await expect(page.getByRole("heading")).toBeVisible();
  await expect(new AxeBuilder({ page }).analyze()).resolves.toMatchObject({ violations: [] });

  await page.getByLabel(/email/i).fill("e2e@example.test");
  await page.getByLabel(/^password$/i).fill("Correct-horse-battery-1");
  await page.getByLabel(/confirm password/i).fill("Correct-horse-battery-1");
  await page.getByRole("button", { name: /create account|sign up|register/i }).click();
  await expect(page).toHaveURL(/\/$/);
});
