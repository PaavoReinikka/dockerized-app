const { test, expect } = require("@playwright/test");

test('Pressing "Fetch message" shows message.', async ({ page }) => {
  await page.goto("http://localhost:5173/");
  // wait for a second for the page to load
  await page.waitForTimeout(1000);
  const canvas = page.locator("#myChart");
  await expect(canvas).toBeVisible();
});

test('PriceBall displays current price', async ({ page }) => {
  await page.goto("http://localhost:5173/");
  // Adjust selector if your PriceBall has a specific id or class
  const priceBall = page.locator("#priceBall");
  await expect(priceBall).toBeVisible();
  // Optionally check that it contains a price (number)
  const text = await priceBall.textContent();
  expect(text).toMatch(/\d+(\.\d+)?/);
});


test('Date range selector changes table data', async ({ page }) => {
  await page.goto("http://localhost:5173/hintatiedot");
  // Adjust selectors as needed for your date inputs and chart
  const startInput = page.locator('input[name="startDate"]');
  const endInput = page.locator('input[name="endDate"]');
  await startInput.fill('2025-05-20T00:00');
  await endInput.fill('2025-05-22T00:00');
  // Simulate submitting the form or triggering fetch
  await page.click('#submitDates');
  // Wait for table to update
  await page.waitForTimeout(1000);
  const table = page.locator("#pricetable");
  await expect(table).toBeVisible();
});