import { expect, test } from "@playwright/test";

test("US3 smoke: login page remains reachable for recovery path", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "TRDIA Login" })).toBeVisible();
});

test("US3 smoke: trading screen renders with authenticated shell", async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem("trdia.accessToken", "e2e-token");
  });
  await page.goto("/trading");

  await expect(page.getByRole("heading", { name: "Trading" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Ejecutar Orden" })).toBeVisible();
});
