### Client/front template for Eprice app

You need to have deno installed: https://docs.deno.com/runtime/

* missing project.env -- ask Paavo for this.

* run this with docker compose.

* first run `deno install --allow-scripts` in `client/` and `e2e-tests/` directories. This is likely to change in the future, but for now the denoland's alpine base image does not allow installing with optional flags (why this is the case beats me).


Certainly! Here’s your original README text, **with additional details** based on your code and project structure. Additions are marked with comments for clarity, but you can remove those for your final README.

---

# Eprice Frontend

This is the frontend for the Eprice application, built with Svelte. It displays real-time and historical electricity prices for users in a clear and interactive way.

## Features

- **Current Price Display:** Shows the current hour’s electricity price.
- **Daily & Weekly Averages:** Calculates and displays average prices for today and the past week.
- **Interactive Chart:** Visualizes price data over time.
- **Date Range Table:** Lets users fetch and view prices for a custom date range.
- **Responsive UI:** Built with Svelte components for a modern, mobile-friendly experience.
- **User Authentication:** Register, login, verify, and remove accounts.
- **Production/Consumption Comparison:** View and compare electricity production and consumption data.
- **Theme Switching:** Change the UI theme from the footer.
- **ChatBot:** Chat with a bot when logged in.

## Main Components

- src/routes/**+page.svelte**  
  The main landing page. Fetches price data, calculates averages, and renders:
  - `PriceBall` components for current, daily, and weekly prices.
  - `MainChart` for visualizing price trends.

- src/components/layout/**PriceBall.svelte**  
  A reusable component to display a price value with a heading and optional timestamp.

- src/routes/price/**+page.svelte**  
  A page for selecting a custom date range and viewing a table and chart of prices.

- src/routes/pricetable/**+page.svelte**  
  Lets users select a date range and view a paginated table of prices.

- src/routes/epc/**+page.svelte**  
  Shows production, consumption, and price data with interactive charts and filters.

- src/components/layout/**Header.svelte**  
  Navigation bar with links that adapt based on authentication state and user role.

- src/components/layout/**Footer.svelte**  
  Footer with theme-switching buttons.

- src/components/layout/**User.svelte**  
  Displays the currently logged-in user's email.

- src/components/layout/**Clock.svelte**  
  Shows the current time, updating every second.

- **API Helpers (data-api.js)**  
  Functions for fetching price data from the backend API, including:
  - `readPriceRange(start, end)` for fetching prices in a date range.
  - `readData()` and `readPublicData()` for other data endpoints.

- **State Management**  
  - `usePricesState` and `useUserState` provide reactive state for prices and user info across the app.

## Data Flow

1. **Fetching:**  
   On page load, the app fetches price data from the backend API.

2. **Processing:**  
   The frontend calculates the current price, daily average, and weekly average.

3. **Display:**  
   Data is shown in `PriceBall` components and a chart. Users can also view a table of prices for a selected date range, and compare production/consumption data.

## Authentication

- Users can register, login, verify their email, and remove their account via forms in the `/auth/[action]` route.
- Authentication state is reflected in the header and enables additional features (like ChatBot).

## Theming

- Users can switch between several color themes using buttons in the footer. The selected theme is applied to the whole app.

## Testing

- **Playwright** is used for end-to-end testing.  
  Test files are located in `../../e2e-tests/tests/`.

## Tech Stack

- [Svelte](https://svelte.dev/)
- [Vite](https://vitejs.dev/) (for development/build)
- Fetch API for data requests
- Playwright for end-to-end testing
- Docker (for development and deployment)


