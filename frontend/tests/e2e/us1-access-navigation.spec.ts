import { test, expect } from "@playwright/test";

test("US1 smoke: login page is reachable", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "TRDIA Login" })).toBeVisible();
});
