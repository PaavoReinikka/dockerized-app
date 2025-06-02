"""
user_repository.py defines the UserRepository class for user-related database operations in the Eprice backend.

The repository provides asynchronous methods for:
- Retrieving user records by email.
- Creating new user accounts with hashed passwords and verification codes.
- Verifying user email addresses using verification codes.
- Updating verification codes for users.

All operations interact directly with a PostgreSQL database using asyncpg for asynchronous access.
This repository is intended to be used by service and controller layers to abstract database logic
from business and API logic.

Dependencies:
- asyncpg for asynchronous PostgreSQL operations.

Intended Usage:
- Instantiate with a database connection URL.
- Use in authentication and user management services for all user-related database actions.
"""
import asyncpg

class UserRepository:
    """
    Repository class for user-related database operations in the Eprice backend.

    Provides asynchronous methods for retrieving, creating, and updating user records,
    as well as verifying user email addresses. Interacts directly with the PostgreSQL
    database using asyncpg.

    Args:
        database_url (str): The database connection URL.
    """
    def __init__(self, database_url: str):
        """
        Initialize the UserRepository with a database connection URL.

        Args:
            database_url (str): The database connection URL.
        """
        self.database_url = database_url

    async def get_user_by_email(self, email: str):
        """
        Retrieve a user record by email address.

        Args:
            email (str): The user's email address.

        Returns:
            Record or None: The user record if found, otherwise None.
        """
        conn = await asyncpg.connect(self.database_url)
        try:
            user = await conn.fetchrow("SELECT * FROM users WHERE email = $1", email)
            return user
        finally:
            await conn.close()
    
    async def create_user(self, email: str, password_hash: str, verification_code: str):
        """
        Create a new user record in the database.

        Args:
            email (str): The user's email address.
            password_hash (str): The hashed password.
            verification_code (str): The email verification code.

        Raises:
            Exception: If the user could not be created.
        """
        conn = await asyncpg.connect(self.database_url)
        try:
            await conn.execute(
                "INSERT INTO users (email, password_hash, verification_code) VALUES ($1, $2, $3)",
                email, password_hash, verification_code
            )
        finally:
            await conn.close()

    async def verify_code(self, email: str, verification_code: str):
        """
        Verify a user's email address using a verification code.

        Args:
            email (str): The user's email address.
            verification_code (str): The verification code to check.

        Returns:
            str: The result of the update operation.
        """
        conn = await asyncpg.connect(self.database_url)
        try:
            result = await conn.execute(
                "UPDATE users SET is_verified = TRUE WHERE email = $1 AND verification_code = $2",
                email, verification_code
            )
            return result
        finally:
            await conn.close()

    async def update_code(self, email: str, new_code: str):
        """
        Update a user's verification code.

        Args:
            email (str): The user's email address.
            new_code (str): The new verification code.

        Raises:
            Exception: If the update operation fails.
        """
        conn = await asyncpg.connect(self.database_url)
        try:
            await conn.execute(
                "UPDATE users SET verification_code = $1 WHERE email = $2",
                new_code, email
            )
        finally:
            await conn.close()

    async def delete_user(self, email: str):
        """
        Remove a user record from the database.

        Args:
            email (str): The user's email address.

        Raises:
            Exception: If the user could not be removed.
        """
        conn = await asyncpg.connect(self.database_url)
        try:
            await conn.execute("DELETE FROM users WHERE email = $1", email)
        finally:
            await conn.close()
