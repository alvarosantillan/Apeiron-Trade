import { expect, test } from "@playwright/test";

test("US2 smoke: dashboard renders in private shell", async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem("trdia.accessToken", "e2e-token");
  });
  await page.goto("/dashboard");

  await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Navegacion privada" })).toBeVisible();
});
