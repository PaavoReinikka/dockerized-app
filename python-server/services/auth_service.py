from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from repositories.user_repository import UserRepository
from config.secrets import JWT_SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_repository.get_user_by_email(email)
        if not user or not self.verify_password(password, user["password_hash"]):
            return None
        return user

    async def register_user(self, email: str, password: str):
        hashed_password = self.get_password_hash(password)
        await self.user_repository.create_user(email, hashed_password)