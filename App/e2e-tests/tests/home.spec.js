const { test, expect } = require("@playwright/test");

test('Home page loads successfully', async ({ page }) => {
  await page.goto("http://localhost:5173/");
  await expect(page).toHaveTitle("Home - Market Electricity Prices Today");
});

test('Home page has the chart visible.', async ({ page }) => {
  await page.goto("http://localhost:5173/");
  await page.waitForTimeout(1000);
  const canvas = page.locator("#mainChart");
  await expect(canvas).toBeVisible();
});

test('Shows correct main heading and date', async ({ page }) => {
  await page.goto("http://localhost:5173/");
  await page.waitForTimeout(1000);
  const heading = page.locator("#main-heading");
  await expect(heading).toContainText("Market Electricity Prices Today");
  const today = new Date().toLocaleDateString('fi-FI', { timeZone: 'Europe/Helsinki' });
  await expect(heading).toContainText(today);
});

test('Shows price cards section', async ({ page }) => {
  await page.goto("http://localhost:5173/");
  await page.waitForTimeout(1000);
  // Assuming PriceCards renders a container with a known class or role
  await expect(page.locator("#max-price-card")).toBeVisible();
  await expect(page.locator("#min-price-card")).toBeVisible();
  await expect(page.locator("#avg-price-card")).toBeVisible();
  await expect(page.locator("#std-price-card")).toBeVisible();
});

test('Shows register prompt when not logged in', async ({ page }) => {
  await page.goto("http://localhost:5173/");
  await page.waitForTimeout(1000);
  const prompt = page.locator("text=Want to see more features and get the full functionality of the app?");
  await expect(prompt).toBeVisible();
});