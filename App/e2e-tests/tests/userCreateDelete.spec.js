const { test, expect } = require('@playwright/test');

test.describe('User Creation and Deletion', () => {
    let email;
    let password;
    let mailToken;

    test.beforeAll(async () => {
        // Create temp account
        const domainRes = await fetch('https://api.mail.tm/domains');
        if (!domainRes.ok) throw new Error('Failed to fetch mail.tm domains');
        const domainData = await domainRes.json();
        const domain = domainData['hydra:member'][0].domain;
        email = `test${Date.now()}@${domain}`;
        password = `TestPassword${Date.now()}`;

        const accountRes = await fetch('https://api.mail.tm/accounts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address: email, password }),
        });
        if (!accountRes.ok) throw new Error('Failed to create mail.tm account');

        // Get mail.tm token for fetching emails
        const tokenRes = await fetch('https://api.mail.tm/token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address: email, password }),
        });
        if (!tokenRes.ok) throw new Error('Failed to retrieve mail.tm token');
        const tokenData = await tokenRes.json();
        mailToken = tokenData.token;
        });

    // Register user and fill in the email and password
    test('Register user', async ({ page }) => {
        await test.step('Go to the register page', async () => {
            await page.goto('http://localhost:5173/auth/register');
        });
        await test.step('Fill in the registration form', async () => {
            await page.fill('input[name="email"]', email);
            await page.fill('input[name="password"]', password);
            await page.click('button[type="submit"]');
        });
        await test.step('Check the verification message', async () => {
            await expect(page.locator('text=Verification has been sent to your email. Please verify your account to continue.')).toBeVisible();
        });
    });

    test('Verify user', async ({ page }) => {
        // Poll for verification email and extract link
        let verificationLink;
        await test.step('Wait for verification email', async () => {
        for (let i = 0; i < 10; i++) {
            await new Promise(r => setTimeout(r, 2000));
            const messagesRes = await fetch('https://api.mail.tm/messages', {
                headers: { Authorization: `Bearer ${mailToken}` },
            });
            const messages = await messagesRes.json();
            if (messages['hydra:member'].length > 0) {
                const msgId = messages['hydra:member'][0].id;
                const msgRes = await fetch(`https://api.mail.tm/messages/${msgId}`, {
                    headers: { Authorization: `Bearer ${mailToken}` },
                });
                const msg = await msgRes.json();
                // Extract the verification link (adjust regex if needed)
                const match = msg.text.match(/http:\/\/localhost:5173\/auth\/verify\?email=[^&]+&code=[A-Z0-9-]+/);
                if (match) {
                    verificationLink = match[0];
                    break;
                }
            }
        }
        expect(verificationLink).toBeTruthy();
    });


        // Visit the verification link
        await test.step('Visit the verification link', async () => {
            await page.goto(verificationLink);
        });
        
        // Click the verify button
        await test.step('Click the verify button', async () => {
            const verifyButton = page.locator('button[type="submit"]');
            await verifyButton.click();
        });
        
         // Check verification success message and the URL
        await test.step('Check verification success message', async () => {
            await expect(page.locator('text=Your email has been verified. You can now login.')).toBeVisible();
            await expect(page).toHaveURL(/\/auth\/login\?is_verified=true/);
        });

    });

    test('Login user', async ({ page }) => {
        await test.step('Go to the login page', async () => {
            await page.goto('http://localhost:5173/auth/login');
        });
        await test.step('Fill in the login form', async () => {
            await page.fill('input[name="email"]', email);
            await page.fill('input[name="password"]', password);
            await page.click('button[type="submit"]');
        });
        await test.step('Check logged in message on page', async () => {
            await expect(page.locator(`Logged in as: ${email}`)).toBeVisible();
        });
        
        
    });

    test('Remove user', async ({ page }) => {
        await test.step('Go to the remove account page', async () => {
            await page.goto('http://localhost:5173/auth/remove');
        });
        await test.step('Fill in the remove account form', async () => {
            await page.fill('input[name="email"]', email);
            await page.fill('input[name="password"]', password);
            await page.click('button[type="submit"]');
        });
        await test.step('Check account removal message', async () => {
            await expect(page.locator('text=Your account has been removed.')).toBeVisible();
        });
        await test.step('Click the confirm removal button', async () => {
            await page.click('button[type="submit"]');
        });
    });

});

