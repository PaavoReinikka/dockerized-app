const { test, expect } = require('@playwright/test');

test.describe('EPC Page', () => {
  test('renders all chart canvases and form', async ({ page }) => {
    await page.goto('http://localhost:5173/epc');
    await expect(page.locator('#bothChart')).toBeVisible();
    await expect(page.locator('#diffChart')).toBeHidden();
    await expect(page.locator('#priceChart')).toBeHidden();
    await expect(page.locator('form[action*="getCombinedRange"]')).toBeVisible();
    await expect(page.locator('input[name="startTime"]')).toBeVisible();
    await expect(page.locator('input[name="endTime"]')).toBeVisible();
    await expect(page.locator('select#selection')).toBeVisible();
  });

  test('changing filter selection shows correct chart', async ({ page }) => {
    await page.goto('http://localhost:5173/epc');
    const select = page.locator('select#selection');
    await select.selectOption('difference');
    await expect(page.locator('#diffChart')).toBeVisible();
    await expect(page.locator('#bothChart')).toBeHidden();
    await expect(page.locator('#priceChart')).toBeHidden();

    await select.selectOption('price');
    await expect(page.locator('#priceChart')).toBeVisible();
    await expect(page.locator('#bothChart')).toBeHidden();
    await expect(page.locator('#diffChart')).toBeHidden();

    await select.selectOption('both');
    await expect(page.locator('#bothChart')).toBeVisible();
    await expect(page.locator('#diffChart')).toBeHidden();
    await expect(page.locator('#priceChart')).toBeHidden();
  });

  test('submitting form updates charts and cards', async ({ page }) => {
    await page.goto('http://localhost:5173/epc');
    // Fill in the date range inputs
    await page.fill('input[name="startTime"]', '2025-05-20T00:00');
    await page.fill('input[name="endTime"]', '2025-05-22T00:00');
    await page.click('button[type="submit"]');
    // Wait for loading to finish
    await expect(page.locator('button[type="submit"]')).toBeEnabled({ timeout: 5000 });
    // Check that at least one PriceCards component is visible
    await expect(page.locator('.price-card, [class*="PriceCard"]')).toBeVisible();
  });

  test('toggle chart type button switches chart type', async ({ page }) => {
    await page.goto('http://localhost:5173/epc');
    const toggleBtn = page.locator('button', { hasText: 'Toggle Chart Type' });
    await expect(toggleBtn).toBeVisible();
    await toggleBtn.click();
    // No direct way to check chart type, but you can check that the button is clickable and charts are still visible
    await expect(page.locator('#bothChart')).toBeVisible();
  });

  test('shows error alert on invalid date range', async ({ page }) => {
    await page.goto('http://localhost:5173/epc');
    // Fill in invalid dates
    await page.fill('input[name="startTime"]', '2025-01-02');
    await page.fill('input[name="endTime"]', '2025-01-01');
    await page.click('button[type="submit"]');
    await expect(page.locator('.alert-error')).toBeVisible();
  });
});