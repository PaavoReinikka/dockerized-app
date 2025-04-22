from fastapi import APIRouter, Response, Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
from models.user_model import User
from config.secrets import DATABASE_URL, JWT_SECRET, ALGORITHM, COOKIE_KEY
import asyncpg


router = APIRouter()
user_repository = UserRepository(DATABASE_URL)
auth_service = AuthService(user_repository)

@router.post("/api/auth/register")
async def register(user: User, response: Response):
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
    db_user = await auth_service.authenticate_user(user.email.lower(), user.password)
    if not db_user:
        # SUGGESTION TO JUHO:
        # dont't raise exceptions, just return set status code and return a message
        # and we can handle it in the front
        #raise HTTPException(status_code=401, detail="Incorrect email or password.")
        response.status_code = 401
        return {"message": "Incorrect email or password."}
    
    payload = {"email": db_user["email"], "id": db_user["id"]}
    token = auth_service.create_access_token(payload)
    response.set_cookie(key=COOKIE_KEY,
                        value=token,
                        httponly=True, samesite="lax",
                        domain="localhost", path="/",
                        secure=False)

    return {"message": "Welcome!"}


def create_jwt_middleware(public_routes):
    """
    Middleware factory to validate JWT token and attach user info to the request.
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