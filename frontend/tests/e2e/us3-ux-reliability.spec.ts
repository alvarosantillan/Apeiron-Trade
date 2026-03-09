import { expect, test } from "@playwright/test";

test("US3 smoke: login page remains reachable for recovery path", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "TRDIA Login" })).toBeVisible();
});
