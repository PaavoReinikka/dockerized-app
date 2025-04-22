from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re

class User(BaseModel):
    email: EmailStr  # Ensures the email is valid
    password: str

    @validator("password")
    def validate_password(cls, password):
        # validate password strength (add more criteria as needed)
        if len(password) < 4:
            raise ValueError("Password must be at least 8 characters long.")
        
        return password