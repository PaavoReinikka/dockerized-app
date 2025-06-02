"""
main.py initializes and configures the FastAPI application for the Eprice backend.

Features:
- Sets up application lifespan events for startup and shutdown, including checking and inserting missing price data on startup.
- Registers custom exception handlers for request validation errors.
- Configures CORS middleware for frontend and test environments.
- Includes routers for authentication and external API endpoints.
- Adds JWT authentication middleware for protected routes.
- Integrates scheduled tasks and ensures graceful shutdown of background schedulers.

Dependencies:
- fastapi for API framework and routing.
- fastapi.middleware.cors for CORS configuration.
- controllers for API route definitions.
- scheduled_tasks for background data synchronization.
- config for application and secret settings.
- models.custom_exception for custom error handling.

Intended Usage:
- Entry point for running the Eprice backend server.
- Should be run with a compatible ASGI server (e.g., uvicorn).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.auth_controller import router as auth_router
from controllers.auth_controller import create_jwt_middleware
from controllers.data_controller import router as external_api_router

from scheduled_tasks.porssisahko_scheduler import shutdown_scheduler, fetch_and_insert_missing_porssisahko_data

import config
from config.secrets import public_routes

from models.custom_exception import custom_validation_exception_handler
from fastapi.exceptions import RequestValidationError

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.
    This function is called when the application starts up and shuts down.
    It is used to perform startup tasks, such as checking for missing data.
    On shutdown, it ensures scheduled tasks are properly terminated.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    # Startup code
    print("Server is starting... Checking for missing data.")
    start_datetime = "2025-05-12T23:00:00"
    await fetch_and_insert_missing_porssisahko_data(start_datetime)
    print("Server started and missing data checked.")
    yield
    # Shutdown code
    shutdown_scheduler()

app = FastAPI(lifespan=lifespan)
app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.include_router(external_api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.middleware("http")(create_jwt_middleware(public_routes))
