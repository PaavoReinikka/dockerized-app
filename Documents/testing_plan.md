# Backend and E2E Testing Plan

---

## 1. Introduction  
This testing plan focuses on backend testing and end-to-end (e2e) testing of the full application. Backend tests are implemented using pytest for asynchronous REST API testing. E2E tests are implemented using Playwright to cover user workflows and frontend functionality.

### 1.1 Scope

#### 1.1.1 In Scope  
- Backend REST API integration tests via pytest.  
- End-to-end testing of critical user flows and UI elements using Playwright.  
- Testing covers authentication flows, data retrieval and display, and interaction with UI components.

#### 1.1.2 Out of Scope  
- Performance, load, and security testing.  
- Manual testing outside automated test suites.

#### 1.1.3 Tested Endpoints and Features

| Endpoint                 | HTTP | Description                                 |
|--------------------------|------|---------------------------------------------|
| /api/auth/register       | POST | User registration                           |
| /api/auth/login          | POST | Login                                      |
| /api/auth/logout         | GET  | Logout                                     |
| /api/public/data         | GET  | Public price data                           |
| /api/data/today          | GET  | Today's price data                          |
| /api/price/range         | POST | Price data for a time range                 |
| /api/price/hourlyavg     | POST | Hourly average prices for a time range      |
| /api/price/weekdayavg    | POST | Weekday average prices for a time range     |
| /api/windpower           | GET  | Wind power production data                  |
| /api/windpower/range     | POST | Wind power production data for a time range |
| /api/consumption         | GET  | Electricity consumption data                |
| /api/consumption/range   | POST | Electricity consumption data for a time range|
| /api/production          | GET  | Total electricity production data           |
| /api/production/range    | POST | Total electricity production data for a time range|

#### 1.1.4 E2E-Tested Features

Implemented Test Cases (by 8.6.2025)

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


#### 1.1.5 Features Missing from E2E-Tests

- epc.spec.js: Testing production and consumption -view with logged in user (data retrieval, interactivity, graph response, price-cards)
- price.spec.js: Testing prices -view with logged in user (data retrieval, interactivity, graph response, price-cards)


### 1.2 Quality Objectives  
- Ensure backend API behaves correctly and reliably.  
- Validate full user journeys through e2e tests to catch integration issues.  
- Test authentication and authorization flows end-to-end.  
- Achieve high test coverage of critical features and UI elements
- Coverage measured by pytest-cov for backend, and Playwrights own coverage tools for frontend (only if time permits).

### 1.3 Roles and Responsibilities  
- All team members are responsible for participating in testing activities, reporting identified bugs, and contributing to bug resolution.

### 1.4 Test Execution in Docker

- All backend and E2E tests are executed in isolated Docker containers.
- Source code for tests is mounted into the containers from `Eprice/App/e2e-tests` and `Eprice/App/backend-tests`.
- The test containers depend on the application and database containers to ensure the environment is ready before tests run.

---

## 2. Test Methodology  

### 2.1 Overview  
- Agile, continuous testing integrated into development pipelines.  
- Backend tested with pytest (async API tests).  
- E2E tests use Playwright to simulate real user interactions in browsers.

### 2.2 Test Levels  
- API-level integration testing (pytest + httpx).  
- End-to-end UI testing (Playwright).  

### 2.3 Bug Triage  
- Prioritize bugs by severity and impact on functionality.  
- Use automated test reports and bug tracking tools.  
- Regular meetings to decide fixes pre-release/-deadline.

### 2.5 Test Completeness  
- All critical backend tests pass.  
- E2E tests cover core user scenarios without failures.  
- Test coverage reports reviewed for completeness.

---

## 3. Test Deliverables  

- Testing plan document  
- pytest backend test scripts  
- Playwright e2e test scripts  
- Automated test reports (pytest-html, Playwright reports)  
- Bug reports and issue tracker entries

---

## 4. Resources & Environment Requirements  

### 4.1 Testing Tools  
- **pytest** + **pytest-asyncio** for backend API tests  
- **httpx.AsyncClient** for async HTTP calls  
- **Playwright** for browser automation and e2e tests  

### 4.2 Test Environment  
- Backend running in test environment or locally  
- Frontend application accessible for UI tests (localhost or test server)  
- Python 3.13+ with dependencies  
- Node.js environment for Playwright tests (Vite is serving the client)

---

## 5. Terms / Acronyms

| TERM/ACRONYM | DEFINITION                           |
|--------------|------------------------------------|
| API          | Application Programming Interface  |
| AUT          | Application Under Test             |
| pytest       | Python testing framework           |
| AsyncClient  | Asynchronous HTTP client for tests |
| E2E          | End-to-End testing                 |
| UI           | User Interface                    |
