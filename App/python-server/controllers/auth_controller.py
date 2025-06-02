""" auth_controller.py defines the authentication controller for the Eprice backend API using FastAPI.
It provides endpoints for user registration, login, logout, email verification, and resending verification codes.
The controller manages authentication logic, JWT token handling, and cookie management for session persistence.

Key Endpoints:

POST /api/auth/register: Registers a new user and sends a confirmation email. Handles duplicate email errors.
POST /api/auth/login: Authenticates a user, checks email verification status, and issues a JWT token as an HTTP-only cookie.
GET /api/auth/logout: Logs out the user by deleting the authentication cookie.
POST /api/auth/verify: Verifies a user's email using a code sent to their email address.
POST /api/auth/resend: Resends the email verification code to the user.
The controller uses dependency-injected service and repository layers for business logic and database access.
It also provides a JWT middleware factory for protecting private routes by validating JWT tokens from cookies and attaching user info to the request state.

Error handling is performed by setting appropriate HTTP status codes and returning informative messages for frontend handling.
All endpoints expect and return JSON payloads.

Dependencies:

FastAPI for API routing and response handling.
jose for JWT encoding/decoding.
asyncpg for async PostgreSQL operations.
Custom modules for user models, authentication services, and configuration.
This controller is intended to be used as part of the FastAPI application and imported into the main app router. """

from fastapi import APIRouter, Response, Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
from models.user_model import User, UserCode, EmailRequest
from config.secrets import DATABASE_URL, JWT_SECRET, ALGORITHM, COOKIE_KEY
import asyncpg


router = APIRouter()
user_repository = UserRepository(DATABASE_URL)
auth_service = AuthService(user_repository)

@router.post("/api/auth/register")
async def register(user: User, response: Response):
    """
    Registers a new user and sends a confirmation email.

    Attempts to create a new user account with the provided email and password.
    If successful, sends a confirmation email with a verification code.
    Handles duplicate email registration and unexpected errors.

    Args:
        user (User): The user registration data (email and password).
        response (Response): FastAPI response object for setting status codes.

    Returns:
        dict: JSON message indicating success or the reason for failure.

    NOTE: email can raise fastapi_mail.errors.ConnectionErrors for SMTP connection issues,
          or some other errors related to email sending.
    """
    try:
        await auth_service.register_user(user.email.lower(), user.password)
        return {"message": f"Confirmation email sent to address {user.email.lower()}."}
    except asyncpg.UniqueViolationError:
        print(f"Email already registered: {user.email.lower()}")
        response.status_code = 400
        return {"message": "Email already registered."}
    except Exception as e:
        print(f"Error during registration: {str(e)}")
        response.status_code = 500
        return {"error": "An error occurred during registration."}

@router.post("/api/auth/login")
async def login(user: User, response: Response):
    """
    Authenticates a user and issues a JWT token as an HTTP-only cookie.

    Verifies the user's email and password. Checks if the user's email is verified.
    If authentication is successful, sets a JWT token in a secure cookie.
    Handles incorrect credentials and unverified email cases.

    Args:
        user (User): The user login data (email and password).
        response (Response): FastAPI response object for setting cookies and status codes.

    Returns:
        dict: JSON message indicating the result of the login attempt.
    """
    db_user = await auth_service.authenticate_user(user.email.lower(), user.password)
    if not db_user:
        # SUGGESTION TO JUHO:
        # dont't raise exceptions, just return set status code and return a message
        # and we can handle it in the front
        #raise HTTPException(status_code=401, detail="Incorrect email or password.")
        response.status_code = 401
        return {"message": "Incorrect email or password."}
    
    if not db_user["is_verified"]:
        print(f"Email not verified: {user.email.lower()}")
        response.status_code = 401
        return {"message": "Email not verified."}

    payload = {"email": db_user["email"], "role": db_user["role"]}
    token = auth_service.create_access_token(payload)
    response.set_cookie(key=COOKIE_KEY,
                        value=token,
                        httponly=True, samesite="lax",
                        path="/",
                        secure=False)
                        #domain="80.221.17.169")

    return {"message": "Welcome!"}


@router.get("/api/auth/logout")
async def logout(response: Response):
    """
    Logs out the current user by deleting the authentication cookie.

    Removes the JWT authentication cookie from the client to end the session.

    Args:
        response (Response): FastAPI response object for deleting cookies.

    Returns:
        dict: JSON message confirming successful logout.
    """
    response.delete_cookie(
        key=COOKIE_KEY,
        path="/",
        #domain="80.221.17.169"
    )
    return {"message": "User has successfully logged out"}

@router.post("/api/auth/verify")
async def verify(user_code: UserCode, response: Response):
    """
    Verifies a user's email address using a verification code.

    Checks the provided verification code against the stored code for the user.
    If valid, marks the user's email as verified. Handles invalid or expired codes.

    Args:
        user_code (UserCode): The user's email and verification code.
        response (Response): FastAPI response object for setting status codes.

    Returns:
        dict: JSON message indicating the result of the verification attempt.
    """
    try:
        await auth_service.verify_user(user_code.email.lower(), user_code.code)
        return {"message": "Email verified successfully."}
    except Exception as e:
        print(f"Error during verification: {str(e)}")
        response.status_code = 400
        return {"message": "Verification failed."}


@router.post("/api/auth/resend")
async def resend_verification_code(request: EmailRequest, response: Response):
    """
    Resends a new email verification code to the user's email address.

    Used when the user did not receive or lost the original verification code.
    Handles errors such as invalid email addresses.

    Args:
        request (EmailRequest): The user's email address.
        response (Response): FastAPI response object for setting status codes.

    Returns:
        dict: JSON message indicating whether the code was resent successfully.

    NOTE: email can raise fastapi_mail.errors.ConnectionErrors for SMTP connection issues,
          or some other errors related to email sending.
    """
    try:
        await auth_service.update_verification_code(request.email.lower())
        return {"message": "Verification code resent successfully."}
    except Exception as e:
        print(f"Error during resending verification code: {str(e)}")
        response.status_code = 400
        return {"message": "Failed to resend verification code."}

@router.post("/api/auth/remove")
async def remove_user(user: User, response: Response):
    """
    Removes a user record from the database.

    Deletes the user account associated with the provided email address.
    Handles errors such as non-existent users. First authenticates the user
    to ensure they have the right to delete the account.

    Args:
        user (User): The user data containing the email address.
        response (Response): FastAPI response object for setting status codes.

    Returns:
        dict: JSON message indicating whether the user was removed successfully.
    """
    db_user = await auth_service.authenticate_user(user.email.lower(), user.password)

    if not db_user:
        print(f"Authentication failed for user: {user.email.lower()}")
        response.status_code = 401
        return {"message": "Authentication failed. Incorrect email or password."}

    try:
        await auth_service.remove_user(user.email.lower())
        return {"message": "User account removed successfully."}
    except asyncpg.NoDataFoundError:
        print(f"Unable to remove user: {user.email.lower()}")
        response.status_code = 404
        return {"message": "User account was not removed -- contact site admin: eprice.varmennus@gmail.com."}

                                   
def create_jwt_middleware(public_routes):
    """
    Creates a FastAPI middleware for validating JWT tokens on protected routes.

    Extracts the JWT token from cookies, decodes and verifies it, and attaches
    the user payload to the request state. Skips validation for public routes and
    handles preflight (OPTIONS) requests. Returns a 401 error if the token is
    missing or invalid.

    Args:
        public_routes (list): List of route paths that do not require authentication.

    Returns:
        Callable: The JWT validation middleware function.
    """
    async def jwt_middleware(request: Request, call_next):
        # Accept preflight requests
        if request.method == "OPTIONS":
            return await call_next(request)

        # Skip validation for public routes
        if request.url.path in public_routes:
            return await call_next(request)

        # Extract token from cookies
        token = request.cookies.get(COOKIE_KEY)
        if not token:
            return JSONResponse(status_code=401, content={"message": "No token found!"})

        # Validate the token
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            request.state.user = payload
        except JWTError:
            return JSONResponse(status_code=401, content={"message": "Invalid token!"})

        # Proceed to the next middleware or route handler
        return await call_next(request)

    return jwt_middleware