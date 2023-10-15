from datetime import datetime, timedelta, timezone
from typing import Annotated

from app.config import jwt_settings
from app.database import get_session
from app.models.users import User as UserModel
from app.schemas.tokens import TokenData
from app.schemas.users import UserCreate as UserCreateSchema
from app.services.users import UsersService, users_service
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import with_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UsersController:
    def __init__(self, users_service: UsersService) -> None:
        self.users_service = users_service

    @with_async_session
    async def register(
        self,
        user_schema: UserModel,
        session: AsyncSession | None = None,
    ) -> None:
        email = user_schema.email
        if await self.users_service.get_user(session=session, email=email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )
        user = UserModel(**user_schema.dict())
        return await self.users_service.create(user=user, session=session)

    @with_async_session
    async def authenticate_user(
        self,
        username: str,
        password: str,
        session: AsyncSession | None,
    ) -> UserModel | HTTPException:
        user = await self.users_service.authenticate_user(username=username, password=password, session=session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    @with_async_session
    async def get_current_user(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession | None = None,
    ) -> UserModel | HTTPException:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, jwt_settings.secret_key, algorithms=[jwt_settings.algorithm])
            username = payload.get("sub")
            if not username:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = await self.users_service.get_user(username=token_data.username, session=session)
        if not user:
            raise credentials_exception
        return user

    async def get_current_active_user(
        self,
        current_user: Annotated[UserModel, Depends(get_current_user)],
    ):
        if current_user.disabled:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        return current_user

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=jwt_settings.access_token_expire_minutes)
        to_encode["exp"] = expire
        return jwt.encode(to_encode, jwt_settings.secret_key, algorithm=jwt_settings.algorithm)


users_controller = UsersController(users_service=users_service)
