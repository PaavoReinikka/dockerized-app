# Svelte Frontend Design: An Overview

## Introduction

The Eprice frontend is built using [Svelte](https://svelte.dev/), a modern JavaScript framework for building fast and reactive user interfaces. The project structure is organized to promote maintainability, scalability, and clear separation of concerns. The frontend communicates with the backend via HTTP APIs and leverages Svelte’s built-in features for routing, state management, and component-based development.

## Directory Structure

The main frontend code resides in `App/client/src`, which is organized as follows:

- **routes/**: SvelteKit routing and server-side logic for each page.
- **lib/**: Shared libraries, including API clients, reusable components, state management, and utility functions.
- **static/**: Static assets such as images and favicon.

## Key Concepts

- **Component-Based UI**: UI is composed of reusable Svelte components (e.g., `ChatBot.svelte`, `PriceCards.svelte`).
- **Routing**: SvelteKit file-based routing handles navigation and server-side logic for each route.
- **State Management**: Shared state is managed using Svelte stores (see `states/`).
- **API Integration**: Communication with the backend is handled via API modules in `lib/apis/`.
- **Server-Side Logic**: `+page.server.js` and `+layout.server.js` files enable server-side data fetching and actions.

---

## Routing and Page Structure

The frontend uses SvelteKit’s file-based routing system, where each file or directory under `src/routes/` corresponds to a route in the application. This enables clear organization of pages and their associated logic:

- **Top-Level Pages:** Each directory (e.g., `/auth`, `/chat`, `/price`, `/epc`, `/logout`, `/send`) represents a distinct page or feature.
- **Server-Side Logic:** Files ending with `.server.js` (e.g., `+page.server.js`, `+layout.server.js`) handle server-side data fetching, form actions, and secure operations.
- **Layouts:** Shared layouts are defined in `+layout.svelte` and `+layout.js`, providing consistent structure and logic across multiple pages.
- **API Routes:** The `api/` directory (e.g., `api/devchat/+server.js`) is used for defining custom backend endpoints that can be called from the frontend. The devchat api is a "mock" api, and it's only purpose is to verify that the developer chat container is up and running (it is not part of production configuration).

This structure allows for both client-side interactivity and secure server-side processing, making it easy to build dynamic and secure web applications.

---

## Components

The UI is built from modular, reusable Svelte components located in `lib/components/`. Each component encapsulates its own markup, styles, and logic, making it easy to compose complex interfaces from simple building blocks.

- **Feature Components:** Components like `ChatBot.svelte`, `PriceCards.svelte`, and the various `ChatView*.svelte` files implement core features and views of the application.
- **Layout Components:** The `layout/` subdirectory contains shared UI elements such as `Header.svelte`, `Footer.svelte`, `Clock.svelte`, and `User.svelte`, which are used across multiple pages for a consistent look and feel.
- **Reusability:** Components are designed to be reusable and composable, allowing for rapid development and easy maintenance.

This approach enables a clear separation of concerns, improves code readability, and supports scalable frontend development.

---

## State Management

State management in the Eprice frontend leverages Svelte's built-in reactivity, which provides a simple way to share state across components. Shared states are organized under `lib/states/`, making it easy to manage application-wide data such as user authentication status or price data.

- **Example – User State:**  
  The `userState.svelte.js` file defines a stateful object for managing the current user's authentication and profile information. This object can be imported and used by any component or page that needs to react to changes in user status (e.g., login, logout, or profile updates).
- **Usage:**  
  Components can follow the `user` state to display user-specific UI or trigger actions when the authentication state changes. For example, the header component can show the user's email when logged in, or a login button otherwise.

We also use stateful variables across the frontend (defined with `$state(<value>)`). It is possible to mix normal variables and Svelte's stateful variables in code, and there are various mechanisms besides stateful variables that allow reactivity -- updating our frontend to fully leverage Svelte's in-built features is a major backlog item. 

---

## API Integration

Communication between the frontend and backend is handled through dedicated API modules located in `lib/apis/`. These modules encapsulate HTTP requests, making it easy for components and pages to interact with backend endpoints in a consistent and reusable way.

- **API Modules:**  
  For example, `data-api.js` provides functions to fetch or send data related to prices or other business logic. By centralizing API calls, the codebase avoids duplication and makes it easier to update endpoints or request logic in one place.

- **Usage in Components and Pages:**  
  Components and pages import these API modules to perform actions such as fetching price data, submitting forms, or handling authentication (*see the subchapter for caviats*). This keeps UI logic separate from data-fetching logic and improves maintainability.

- **Error Handling:**  
  API modules can include error handling to ensure that failures are managed gracefully and meaningful feedback is provided to the user interface.

This approach ensures a clear separation between UI and data access logic, supports code reuse, and simplifies future changes to backend communication.

---

### Note on API Call Encapsulation

While the ideal approach is to encapsulate all API calls within modules under `lib/apis/` and import them wherever needed, time constraints during development led to a pragmatic divergence from this pattern. In the current implementation, many server-side API calls are defined directly within the corresponding `+page.server.js` files, rather than being abstracted into reusable modules.

- **Current Approach:**  
  For example, in the `price/` and `epc/` routes, the logic for fetching or posting data to the backend is written directly inside the `+page.server.js` files. This means that data-fetching and business logic are mixed with route handling, which can make the code harder to maintain and reuse.

- **Backlog / To-Do:**  
  Refactoring these server-side API calls into dedicated modules under `lib/apis/` is a planned improvement. This would bring the server-side code in line with the client-side pattern, promoting better separation of concerns, easier testing, and improved maintainability.

This divergence is a known technical debt and is tracked as a backlog item for future development.

---

## Client Directory Structure and Route Purposes

Here’s a high-level overview of `App/client/src` -- the directory is organized to support a modular and scalable frontend:

- **routes/**  
  Contains all the application routes. Each subdirectory or file corresponds to a page or API endpoint:
  - `/auth/` – Handles user authentication (login, register, verification.).
  - `/chat/` – Provides the chat interface and related features.
  - `/price/` – First main view, allows user to retrieve price data and visualize it in various ways.
  - `/epc/` – Second main view,  allows user to retrieve consumption/production data and visualize it in various ways.
  - `/logout/` – Manages user logout functionality.
  - `/send/` – Handles re-sending email verification.
  - `/api/` – Contains custom API endpoints for internal or development use (e.g., `devchat`).

- **lib/**  
  Shared code and resources:
  - `apis/` – API client modules for backend communication.
  - `components/` – Reusable Svelte UI components.
  - `states/` – For state management across pages and components.
  - `utils/` – Utility/helper functions.
  - `assets/` – Static assets like images.

- **static/**  
  Public static files (e.g., favicon, images) served directly by the frontend.

This structure supports clear separation of concerns, making it easier to maintain, extend, and onboard new contributors. Each route directory typically contains:
- `+page.svelte` for the UI,
- `+page.server.js` for server-side logic,
- and optionally `+page.js` for client-side logic.

---

## Global Styles and UI Frameworks

The frontend also includes global configuration and styling files at the root of the `client` directory:

- **app.css**  
  This file contains global CSS styles that apply to the entire application. It is the main entry point for custom styles and for importing third-party CSS frameworks.

- **app.html**  
  The HTML template for the application. It defines the base structure of the HTML document, including where the Svelte app is mounted.

- We also use `<style>` blocks here and there in our pages and compoenents. Moving all these in global `app.css` is also a backlog item.

### UI Frameworks

- **Tailwind CSS**  
  The project uses [Tailwind CSS](https://tailwindcss.com/) for utility-first, responsive styling. Tailwind classes are used throughout Svelte components to rapidly build custom designs without leaving the markup.

- **Skeleton UI**  
  [Skeleton](https://www.skeleton.dev/) (via Skeleton Labs) is integrated for ready-made, accessible UI components and design tokens. This helps maintain a consistent look and feel while speeding up development.

These tools and files ensure a consistent, modern, and customizable user interface across the application.

---