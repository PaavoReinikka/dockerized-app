"""
secrets.py

Configuration and secrets for the Eprice backend.

This module loads environment variables for database, JWT, and email settings.
It also defines the list of public routes that do not require authentication.
"""

import os

# Database configuration
# check if environment variables for postgres are set, otherwise use default values
# Default values are for development purposes only
# and should not be used in production

if os.getenv("POSTGRES_USER") is None:
    os.environ["POSTGRES_USER"] = "username"
if os.getenv("POSTGRES_PASSWORD") is None:
    os.environ["POSTGRES_PASSWORD"] = "password"
if os.getenv("PGHOST") is None:
    os.environ["PGHOST"] = "postgresql_database"
if os.getenv("PGPORT") is None:
    os.environ["PGPORT"] = "5432"
if os.getenv("POSTGRES_DB") is None:
    os.environ["POSTGRES_DB"] = "database"

# PostgreSQL connection string
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('POSTGRES_DB')}"
# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "wsd-project-secret")  # Default value for development
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Default algorithm
COOKIE_KEY = os.getenv("COOKIE_KEY", "token")  # Default cookie key
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

MAIL_USERNAME=os.getenv("MAIL_USERNAME", "eprice.varmennus@gmail.com")  # Default sender
MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")  # Default password
MAIL_FROM=os.getenv("MAIL_FROM", "eprice.varmennus@gmail.com")  # Default sender email
MAIL_PORT=os.getenv("MAIL_PORT", 587)  # Default port for TLS
MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com")  # Default SMTP server
MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME", "Eprice-verification")


# Public routes that do not require authentication
# These routes can be accessed without a valid JWT token
public_routes = [
    "/api/public/data",
    "/api/auth/login",
    "/api/auth/register",
    "/api/auth/verify",
    "/api/auth/resend",
    "/api/auth/logout",
    "/api/auth/remove",
    #"/docs",
    "/openapi.json",
    "/api/price/range",
    ]