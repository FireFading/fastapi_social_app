from datetime import datetime, timedelta, timezone

from app.config import jwt_settings
from app.exceptions.users import (
    InactiveUserException,
    InsufficientCredentialsException,
    UnauthorizedException,
    UserExistsException,
)
from app.models.users import User as UserModel
from app.schemas.users import UserCreate as UserCreateSchema
from app.schemas.users import UserUpdate as UserUpdateSchema
from app.services.users import UsersService, users_service
from fastapi import HTTPException
from jose import JWTError, jwt


class UsersController:
    def __init__(self, users_service: UsersService) -> None:
        self.users_service = users_service

    async def register(
        self,
        user_schema: UserCreateSchema,
    ) -> UserModel | HTTPException:
        email = user_schema.email
        if await self.users_service.get_user(email=email):
            raise UserExistsException()
        user = UserModel(**user_schema.model_dump())
        return await self.users_service.create(user=user)

    async def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> UserModel | HTTPException:
        user = await self.users_service.authenticate_user(username=username, password=password)
        if not user:
            raise UnauthorizedException()
        return user

    async def update_user_info(self, user: UserModel, update_user_schema: UserUpdateSchema) -> UserModel:
        user.full_name = update_user_schema.full_name
        user.email = update_user_schema.email
        return await self.users_service.update_info(user=user)

    async def verify_token(
        self,
        token: str,
        token_type: str = "access",
    ):
        try:
            payload = jwt.decode(
                token=token,
                key=jwt_settings.secret_key if token_type == "access" else jwt_settings.refresh_secret_key,
                algorithms=[jwt_settings.algorithm],
            )

            token_exp = payload.get("exp")
            if not token_exp:
                raise InsufficientCredentialsException()

            now = datetime.now(timezone.utc)
            if now > datetime.fromtimestamp(token_exp, tz=timezone.utc):
                raise InsufficientCredentialsException()
            username = payload.get("sub")
            if not username:
                raise InsufficientCredentialsException()

        except JWTError:
            raise InsufficientCredentialsException()
        user = await self.users_service.get_user(username=username)
        if not user:
            raise InsufficientCredentialsException()
        if user.is_disabled:
            raise InactiveUserException()
        return user

    def create_token(self, subject: str, token_type: str = "access") -> str:
        expires_delta = (
            jwt_settings.access_token_expire_minutes
            if token_type == "access"
            else jwt_settings.refresh_token_expire_minutes
        )
        expires_in = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
        to_encode = {"exp": expires_in, "sub": subject}
        secret_key = jwt_settings.secret_key if token_type == "access" else jwt_settings.refresh_secret_key
        return jwt.encode(to_encode, key=secret_key, algorithm=jwt_settings.algorithm)


users_controller = UsersController(users_service=users_service)
