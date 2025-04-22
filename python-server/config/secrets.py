import os
import dotenv

# dotenv.load_dotenv()
# Database configuration for development purposes only
# and should not be used in production.
# Project level .env file sets these.


if os.getenv("POSTGRES_USER") is None:
    os.environ["POSTGRES_USER"] = "username"
if os.getenv("POSTGRES_PASSWORD") is None:
    os.environ["POSTGRES_PASSWORD"] = "password"
if os.getenv("PGHOST") is None:
    os.environ["PGHOST"] = "database"
if os.getenv("PGPORT") is None:
    os.environ["PGPORT"] = "5432"
if os.getenv("POSTGRES_DB") is None:
    os.environ["POSTGRES_DB"] = "database"

# PostgreSQL connection string
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('POSTGRES_DB')}"
# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "default-development-secret")  # Default value for development
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Default algorithm
COOKIE_KEY = os.getenv("COOKIE_KEY", "token")  # Default cookie key
ACCESS_TOKEN_EXPIRE_MINUTES = 60
