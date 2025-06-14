# Playwright E2E Tests

This directory contains end-to-end (E2E) tests for the Eprice application, using [Playwright](https://playwright.dev/).  
Tests are designed to run in a Docker container as part of the CI/CD pipeline or for local development.

## How to Run

Build with:

```bash
docker compose up --build -d e2e-tests
```

Run with:

```bash
docker compose run --rm --entrypoint=npx e2e-tests playwright test
```

## Implemented Test Cases

**Authentication** (auth.spec.js):
- Login
    - Shows error on login with invalid credentials
    - Shows error on login with incorrect password
    - Logs in successfully with valid credentials
    - Shows user email after login
    - Logs out successfully

- Register
    - Registers a new user successfully and removes the account after
    - Shows error on register with existing email
    - Shows error on register with insufficient password
    - Shows error on register with invalid email

- Header Navigation Visibility
    - Shows login and register links when not logged in
    - Shows user links and hides login/register when logged in as user
    - Shows Developer Chat link when logged in as admin and devChatAvailable
    - Does not show Developer Chat link for normal user


**Home Page** (home.spec.js):
- Home page loads successfully (title check)
- Home page has the chart visible
- Shows correct main heading and date
- Shows price cards section (max, min, avg, std)
- Shows register prompt when not logged in

## Adding New Tests

Add new test files to the tests/ directory.

Refer to existing tests for structure and best practices.

**Missing** (these are for minimum functionality tests):
- epc.spec.js: Testing production and consumption -view with logged in user (data retrieval, interactivity, graph response, price-cards)
- price.spec.js: Testing prices -view with logged in user (data retrieval, interactivity, graph response, price-cards)


## Notes

- Test users and credentials are defined in each test file.
- Some tests mock API endpoints (e.g., /api/devchat) for deterministic results.
- Make sure the backend and frontend services are running and accessible at the expected URLs before running tests.