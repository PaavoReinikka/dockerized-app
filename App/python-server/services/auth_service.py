"""
auth_service.py defines AuthService, which provides authentication and user management logic for the Eprice backend.

This service handles password hashing and verification, JWT token creation, user authentication,
registration, email verification, and verification code management. It interacts with the user
repository for database operations and with email utilities for sending verification codes.

Key Responsibilities:
- Securely hash and verify user passwords using bcrypt.
- Generate and validate JWT access tokens for authenticated sessions.
- Register new users, including generating and emailing verification codes.
- Authenticate users by verifying credentials.
- Verify user email addresses using codes sent via email.
- Regenerate and resend verification codes as needed.

Dependencies:
- passlib for password hashing.
- jose for JWT encoding.
- async database repository for user data.
- email utilities for sending verification codes.

Intended Usage:
- Instantiated with a UserRepository instance.
- Used by FastAPI controllers to perform authentication-related operations.
"""

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import random
import string
from repositories.user_repository import UserRepository
from config.secrets import JWT_SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from utils.email_tools import send_email_async

class AuthService:
    """
    Service class for authentication and user management logic in the Eprice backend.

    Handles password hashing and verification, JWT token creation, user authentication,
    registration, email verification, and verification code management. Interacts with the
    user repository for database operations and with email utilities for sending verification codes.

    Args:
        user_repository (UserRepository): The repository instance for user database operations.
    """
    def __init__(self, user_repository: UserRepository):
        """
        Initialize the AuthService with a user repository.

        Args:
            user_repository (UserRepository): The repository instance for user database operations.
        """
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        """
        Hash a plaintext password using bcrypt.

        Args:
            password (str): The plaintext password.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)
    
    def generate_verification_code(self):
        """
        Generate a random verification code in the format ABC-123.

        Returns:
            str: The generated verification code.
        """
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits = ''.join(random.choices(string.digits, k=3))
        return f"{letters}-{digits}"

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plaintext password against a hashed password.

        Args:
            plain_password (str): The plaintext password.
            hashed_password (str): The hashed password.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        """
        Create a JWT access token for the given data.

        Args:
            data (dict): The payload data to encode in the token.
            expires_delta (timedelta, optional): Token expiration time. Defaults to configured value.

        Returns:
            str: The encoded JWT token.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

    async def authenticate_user(self, email: str, password: str):
        """
        Authenticate a user by email and password.

        Args:
            email (str): The user's email address.
            password (str): The user's plaintext password.

        Returns:
            dict or None: The user record if authentication succeeds, None otherwise.
        """
        user = await self.user_repository.get_user_by_email(email)
        if not user or not self.verify_password(password, user["password_hash"]):
            return None
        return user

    async def register_user(self, email: str, password: str):
        """
        Register a new user and send a verification code via email.

        Args:
            email (str): The user's email address.
            password (str): The user's plaintext password.

        Raises:
            Exception: If user creation fails.
        """
        hashed_password = self.get_password_hash(password)
        code = self.generate_verification_code()
        
        await self.user_repository.create_user(email, hashed_password, code)
        # Only send email if user creation succeeded
        await send_email_async(email, code)

    async def verify_user(self, email: str, code: str):
        """
        Verify a user's email address using a verification code.

        Args:
            email (str): The user's email address.
            code (str): The verification code.

        Raises:
            Exception: If verification fails.
        """
        result = await self.user_repository.verify_code(email, code)
        if not result:
            raise Exception("Verification failed")
        
    async def update_verification_code(self, email: str):
        """
        Generate and update a new verification code for the user, and send it via email.

        Args:
            email (str): The user's email address.

        Raises:
            Exception: If updating the code fails.
        """
        new_code = self.generate_verification_code()
        await self.user_repository.update_code(email, new_code)
        # Only send email if update succeeded
        await send_email_async(email, new_code)
        
    async def remove_user(self, email: str):
        """
        Remove a user from the database.

        Args:
            email (str): The user's email address.

        Raises:
            Exception: If user removal fails.
        """
        await self.user_repository.delete_user(email)
        