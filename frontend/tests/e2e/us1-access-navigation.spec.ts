import { test, expect } from "@playwright/test";

test("US1 smoke: login page is reachable", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "TRDIA Login" })).toBeVisible();
});

test("US1 smoke: private shell shows navigation when token exists", async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem("trdia.accessToken", "e2e-token");
  });
  await page.goto("/dashboard");

  await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Navegacion privada" })).toBeVisible();
  await expect(page.getByRole("link", { name: "Trading" })).toBeVisible();
});
