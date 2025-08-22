import { test, expect } from "@playwright/test";

const APP = process.env.APP_URL || "http://localhost:5173";

test("smoke: page de login visible", async ({ page }) => {
  await page.goto(APP);
  await expect(page.getByText("Connexion")).toBeVisible();
});

test("protected: redirection vers login", async ({ page }) => {
  await page.goto(APP + "/users");
  await expect(page.getByText("Connexion")).toBeVisible();
});

// Optionnel: test avec backend reel si E2E_WITH_BACKEND=1
// Admin doit exister: admin@example.com / admin
const WITH_BACKEND = process.env.E2E_WITH_BACKEND === "1";
(WITH_BACKEND ? test : test.skip)("login + dashboard", async ({ page }) => {
  await page.goto(APP);
  await page.getByPlaceholder("Email").fill("admin@example.com");
  await page.getByPlaceholder("Mot de passe").fill("admin");
  await page.getByRole("button", { name: "Se connecter" }).click();
  await expect(page.getByText("Dashboard")).toBeVisible();
});
