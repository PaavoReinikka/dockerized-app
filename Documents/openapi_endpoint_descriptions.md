# Eprice API Endpoint Overview

This document provides a concise technical overview of the main API endpoints exposed by the Eprice backend, as described in the OpenAPI specification.  
The API is organized into **public data endpoints** (for electricity, etc.) and **authentication endpoints**.  
All other endpoints require authentication via JWT.

The API is designed for both public and authenticated use. Public endpoints provide enough data for basic electricity price queries and user authentication, while authenticated endpoints allow access to more detailed or user-specific data.

- The use of POST for range queries (instead of GET with query parameters) allows for more complex request bodies and easier extension in the future.
- The API is well-structured for integration with frontend applications and external systems.

---

## Public Endpoints

These endpoints are accessible **without authentication** (no JWT required):

### Electricity Data endpoint

- **GET `/api/public/data`**  
  Returns a list of market price data points (historical and/or current).  
  **Response:** Array of objects with `startDate` (RFC 3339 UTC string) and `price` (euro cents).

### Authentication endpoints

- **POST `/api/auth/register`**  
  Registers a new user.  
  **Request:** JSON with `email` and `password`.  
  **Response:** Confirmation or validation error.

- **POST `/api/auth/login`**  
  Authenticates a user and returns a JWT (usually set as a cookie).  
  **Request:** JSON with `email` and `password`.  
  **Response:** Confirmation or validation error.

- **POST `/api/auth/verify`**  
  Verifies a user by checking the verification code.  
  **Request:** JSON with `email` and `code`.  
  **Response:** Confirmation or validation error.

- **POST `/api/auth/resend`**  
  Resends the verification code to the user's email.  
  **Request:** JSON with `email`.  
  **Response:** Confirmation or validation error.

- **GET `/api/auth/logout`**  
  Logs out the user by clearing the JWT cookie.  
  **Response:** Confirmation.

---

## Protected Data Endpoints

The following endpoints **require authentication** (JWT):

### Market Price data endpoint

- **GET `/api/data/today`**  
  Returns today's market price data points.  
  **Response:** Array of objects with `startDate` and `price`.

- **POST `/api/price/range`**  
  Returns market price data for a specified time range.  
  **Request:** JSON with `startTime` and `endTime` (RFC 3339).  
  **Response:** Array of price data points.

### Wind Power data endpoint

- **GET `/api/windpower`**  
  Returns the latest wind power production forecast.  
  **Response:** Object with `startTime`, `endTime`, and `value`.

- **POST `/api/windpower/range`**  
  Returns wind power production data for a given time range.  
  **Request:** JSON with `startTime` and `endTime` (RFC 3339).  
  **Response:** Array of forecast data points.

### Consumption data endpoint

- **GET `/api/consumption`**  
  Returns the latest electricity consumption forecast.  
  **Response:** Object with `startTime`, `endTime`, and `value`.

- **POST `/api/consumption/range`**  
  Returns consumption data for a given time range.  
  **Request:** JSON with `startTime` and `endTime` (RFC 3339).  
  **Response:** Array of consumption data points.

### Production data endpoint

- **GET `/api/production`**  
  Returns the latest electricity production forecast.  
  **Response:** Object with `startTime`, `endTime`, and `value`.

- **POST `/api/production/range`**  
  Returns production data for a given time range.  
  **Request:** JSON with `startTime` and `endTime` (RFC 3339).  
  **Response:** Array of production data points.

---

## General Notes about api endpoints

- **Validation:**  
  Most endpoints validate input and return a 422 error for malformed requests.

- **Error Handling:**  
  On server errors, endpoints return a 500 status with an error message.

- **Authentication:**  
  Only the endpoints listed under "Public Endpoints" are accessible without a JWT.  
  All other endpoints require authentication.

- **Data Format:**  
  All timestamps are in RFC 3339 UTC format. Numeric values are typically floats (e.g., price, temperature).

---

## API Docs

- **GET `/docs`**  
  API documentation (Swagger UI).

- **GET `/openapi.json`**  
  OpenAPI specification in JSON format.

