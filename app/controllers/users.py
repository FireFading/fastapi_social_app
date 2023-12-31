from datetime import datetime, timedelta, timezone

from app.config import jwt_settings
from app.exceptions.users import (
    InactiveUserException,
    InsufficientCredentialsException,
    PasswordsMismatchException,
    UnauthorizedException,
    UserExistsException,
    UserNotFoundException,
)
from app.models.users import User as UserModel
from app.schemas.users import ResetPassword as ResetPasswordSchema
from app.schemas.users import UpdatePassword as UpdatePasswordSchema
from app.schemas.users import UserCreate as UserCreateSchema
from app.schemas.users import UserUpdate as UserUpdateSchema
from app.services.users import UsersService, users_service
from fastapi import HTTPException, UploadFile
from jose import JWTError, jwt


class UsersController:
    def __init__(self, users_service: UsersService) -> None:
        self.users_service = users_service

    async def get_user_or_404(self, email: str) -> UserModel | HTTPException:
        user = await self.users_service.get_user(email=email)
        if not user:
            raise UserNotFoundException()
        return user

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
        return await self.users_service.update(user=user)

    async def change_password(self, user: UserModel, data: UpdatePasswordSchema) -> UserModel:
        await self.authenticate_user(username=user.username, password=data.old_password)
        if data.password != data.new_password:
            raise PasswordsMismatchException()
        user.password = self.users_service.get_password_hash(password=data.password)
        return await self.users_service.update(user=user)

    async def reset_password(self, token: str, data: ResetPasswordSchema):
        if data.password != data.confirm_password:
            raise PasswordsMismatchException()
        user = await self.verify_token(token=token, token_type="reset")
        user.password = self.users_service.get_password_hash(password=data.password)
        return await self.users_service.update(user=user)

    async def search_users(self, data: str) -> list[UserModel] | None:
        return await self.users_service.search_users(username__contains=data)

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
            sub = payload.get("sub")
            print(sub)
            if not sub:
                raise InsufficientCredentialsException()

        except JWTError:
            raise InsufficientCredentialsException()
        if token_type == "reset":
            return await self.users_service.get_user(email=sub)
        else:
            user = await self.users_service.get_user(username=sub)
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

    async def update_avatar(self, user: UserModel, photo: UploadFile) -> UserModel:
        return await self.users_service.update_avatar(user=user, photo=photo)

    def get_avatar(self, user: UserModel) -> str | None:
        return self.users_service.get_avatar(user=user)

    def delete_avatar(self, user: UserModel):
        self.users_service.delete_avatar(user=user)


users_controller = UsersController(users_service=users_service)
