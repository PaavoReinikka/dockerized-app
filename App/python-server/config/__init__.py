"""
config package initializer

Loads environment variables from .env files for the Eprice backend.
"""


import dotenv
dotenv.load_dotenv(".env.development")
dotenv.load_dotenv(".env.local")
