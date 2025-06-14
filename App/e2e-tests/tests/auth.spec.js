const { test, expect } = require("@playwright/test");
const baseUrl = "http://localhost:5173";

// Test user constants
const USERS = {
    admin: { email: "test@test.com", password: "secret" },
    user: { email: "testi@testi.fi", password: "salaisuus" }
};

// Helper functions
const login = async (page, { email, password }) => {
    await page.goto(`${baseUrl}/auth/login`);
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', password);
    await page.click('button[type="submit"]');
}

const logout = async (page) => {
    await page.goto(`${baseUrl}/`);
    await page.click('#logout-link');
    await expect(page).toHaveURL(`${baseUrl}/logout`);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(`${baseUrl}/`);
}

test.describe("Authentication", () => {
    test("Shows error on login with invalid credentials", async ({ page }) => {
        await login(page, { email: "notarealuser@example.com", password: "wrongpassword" });
        await page.waitForTimeout(1000);
        await expect(page.locator("text=Incorrect email or password")).toBeVisible();
    });

    test("Shows error on login with incorrect password", async ({ page }) => {
        await login(page, { email: USERS.user.email, password: "canada" });
        await page.waitForTimeout(1000);
        await expect(page.locator("text=Incorrect email or password")).toBeVisible();
    });

    test("Registers a new user successfully and removes the account after", async ({ page }) => {
        const email = `testuser${Date.now()}@example.com`;
        await page.goto(`${baseUrl}/auth/register`);
        await page.fill('input[name="email"]', email);
        await page.fill('input[name="password"]', "TestPassword123!");
        await page.click('button[type="submit"]');
        await expect(page.locator("text=Verification has been sent to your email")).toBeVisible();

        // remove the user after test to avoid conflicts
        await page.goto(`${baseUrl}/auth/remove`);
        await page.fill('input[name="email"]', email);
        await page.fill('input[name="password"]', "TestPassword123!");
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(`${baseUrl}/logout?removed=true`);
        await expect(page.locator("text=Your account has been removed")).toBeVisible();
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(`${baseUrl}/`);
    });

    test("Shows error on register with existing email", async ({ page }) => {
        await page.goto(`${baseUrl}/auth/register`);
        await page.fill('input[name="email"]', USERS.user.email);
        await page.fill('input[name="password"]', "TestPassword123!");
        await page.click('button[type="submit"]');
        await expect(page.locator("text=Email already registered.")).toBeVisible();
    });

    test("Shows error on register with insufficient password", async ({ page }) => {
        const email = `testuser${Date.now()}@example.com`;
        await page.goto(`${baseUrl}/auth/register`);
        await page.fill('input[name="email"]', email);
        await page.fill('input[name="password"]', "123");
        await page.click('button[type="submit"]');
        await expect(page.locator("text=Password must be at least 4 characters long")).toBeVisible();
    });

    test("Shows error on register with invalid email", async ({ page }) => {
        const email = `example@bademail`;
        await page.goto(`${baseUrl}/auth/register`);
        await page.fill('input[name="email"]', email);
        await page.fill('input[name="password"]', "TestPassword123!");
        await page.click('button[type="submit"]');
        await expect(page.locator("text=value is not a valid email address")).toBeVisible();
    });

    test("Logs in successfully with valid credentials", async ({ page }) => {
        await login(page, USERS.user);
        await expect(page.locator("text=Welcome")).toBeVisible();
    });

    test("Shows user email after login", async ({ page }) => {
        await login(page, USERS.user);
        await expect(page.locator("#user-info")).toHaveText(`Logged in as: ${USERS.user.email}`);
    });

    test("Logs out successfully", async ({ page }) => {
        await login(page, USERS.user);
        await logout(page);
        await expect(page.locator("#user-info")).toHaveCount(0);
    });

});

test.describe("Header navigation visibility", () => {
    test("Shows login and register links when not logged in", async ({ page }) => {
        await page.goto(`${baseUrl}/`);
        await page.waitForTimeout(1000);
        await expect(page.locator("#login-link")).toBeVisible();
        await expect(page.locator("#register-link")).toBeVisible();
        await expect(page.locator("#logout-link")).toHaveCount(0);
        await expect(page.locator("#delete-link")).toHaveCount(0);
        await expect(page.locator("#epc-link")).toHaveCount(0);
        await expect(page.locator("#price-link")).toHaveCount(0);
        await expect(page.locator("#developer-chat-link")).toHaveCount(0);
    });

    test("Shows user links and hides login/register when logged in as user", async ({ page }) => {
        await login(page, USERS.user);
        await page.goto(`${baseUrl}/`);
        await page.waitForTimeout(1000);
        await expect(page.locator("#login-link")).toHaveCount(0);
        await expect(page.locator("#register-link")).toHaveCount(0);
        await expect(page.locator("#logout-link")).toBeVisible();
        await expect(page.locator("#delete-link")).toBeVisible();
        await expect(page.locator("#epc-link")).toBeVisible();
        await expect(page.locator("#price-link")).toBeVisible();
        await expect(page.locator("#developer-chat-link")).toHaveCount(0);
    });

    test("Shows Developer Chat link when logged in as admin and devChatAvailable", async ({ page }) => {
        await page.route('**/api/devchat', route => {
            route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({ available: true }),
            });
        });
        await login(page, USERS.admin);
        await page.goto(`${baseUrl}/`);
        await page.waitForSelector("#developer-chat-link", { timeout: 5000 });
        await expect(page.locator("#developer-chat-link")).toBeVisible();
    });

    test("Does not show Developer Chat link for normal user", async ({ page }) => {
        await login(page, USERS.user);
        await page.goto(`${baseUrl}/`);
        await expect(page.locator("#developer-chat-link")).toHaveCount(0);
    });
});
