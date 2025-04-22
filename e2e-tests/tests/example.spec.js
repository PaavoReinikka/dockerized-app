const { test, expect } = require("@playwright/test");

test('Pressing "Fetch message" shows message.', async ({ page }) => {
  await page.goto("http://localhost:5173/");
  // wait for a second for the page to load
  await page.waitForTimeout(1000);
  const canvas = page.locator("#myChart");
  await expect(canvas).toBeVisible();
});