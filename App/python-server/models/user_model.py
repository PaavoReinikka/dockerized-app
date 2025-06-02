"""
user_model.py defines Pydantic models for user-related data validation in the Eprice backend.

Models:
- EmailRequest: Validates and represents an email address for requests such as verification code resending.
- UserCode: Validates an email and a verification code, ensuring the code matches the required format (ABC-123).
- User: Validates user registration and login data, enforcing email format and password strength.

All models use Pydantic for type validation and include custom field validators for additional constraints.

Intended Usage:
- Used in FastAPI route handlers for request body validation.
- Ensures consistent and secure data formats for authentication and user management endpoints.
"""
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from pydantic_core import PydanticCustomError
from typing import Optional
import re

class EmailRequest(BaseModel):
    """
    Pydantic model for validating an email address in request bodies.
    This can be extended with additional validation rules as needed.

    Attributes:
        email (EmailStr): The user's email address.
    
    Raises:
        ValidationError: If the email address is not valid.
        Custom exception handler is set up in the main(entrypoint) file.
    """
    email: EmailStr

class UserCode(BaseModel):
    """
    Pydantic model for validating an email and verification code.

    Attributes:
        email (EmailStr): The user's email address.
        code (str): The verification code in format ABC-123.
    """
    email: EmailStr
    code: str

    @field_validator('code')
    def validate_code(cls, code: str) -> str:
        """
        Validate that the verification code matches the required format (ABC-123).

        Args:
            code (str): The verification code to validate.

        Returns:
            str: The validated code.

        Raises:
            ValidationError: If the code does not match the required format.
            Custom exception handler is set up in the main(entrypoint) file.
        """
        pattern = r'^[A-Z]{3}-\d{3}$'
        if not re.match(pattern, code):
            assert 0>10, "Invalid code format. Expected format: ABC-123"
        return code

class User(BaseModel):
    """
    Pydantic model for validating user registration and login data.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
    password: str

    @field_validator('password')
    def validate_password(cls, password: str) -> str:
        """
        Validate that the password meets minimum strength requirements.

        Args:
            password (str): The password to validate.

        Returns:
            str: The validated password.

        Raises:
            ValidationError: If the password does not meet the minimum length requirement.
            Custom exception handler is set up in the main(entrypoint) file.
        """
        assert len(password) >= 4, "Password must be at least 4 characters long"
        return password