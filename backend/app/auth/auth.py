from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from database.schemas import UserCreate, Token, User
from app.database.models import User as DBUser
from app.database.database import get_db
from crud.crud import UserCRUD
from core.config import settings
from core.exceptions import UserNotFoundError, InvalidCredentialsError

class AuthService:
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.access_token_expire_minutes))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def authenticate_user(self, db: AsyncSession, username: str, password: str) -> DBUser:
        user_crud = UserCRUD(db)
        user = await user_crud.get_user_by_username(username)
        if not user:
            raise UserNotFoundError()
        if not await self.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        return user

    async def get_current_user(self, db: AsyncSession, token: str) -> DBUser:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user_crud = UserCRUD(db)
        user = await user_crud.get_user_by_username(username)
        if user is None:
            raise credentials_exception
        return user
