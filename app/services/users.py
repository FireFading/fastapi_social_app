from app.database import with_async_session
from app.models.users import User as UserModel
from app.repositories.users import UsersRepository, users_repository
from fastapi import UploadFile
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersService:
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    @with_async_session
    async def get_user(self, session: AsyncSession | None = None, **kwargs) -> UserModel | None:
        return await self.users_repository.get(session=session, **kwargs)

    @with_async_session
    async def search_users(self, session: AsyncSession | None = None, **kwargs) -> list[UserModel] | None:
        return await self.users_repository.filter(session=session, **kwargs)

    @with_async_session
    async def create(self, user: UserModel, session: AsyncSession | None = None) -> UserModel:
        user.password = self.get_password_hash(user.password)
        return await self.users_repository.create(instance=user, session=session)

    @with_async_session
    async def authenticate_user(
        self, username: str, password: str, session: AsyncSession | None = None
    ) -> UserModel | bool:
        user = await self.users_repository.get(session=session, username=username)
        if not user:
            return False
        return user if self.verify_password(plain_password=password, hashed_password=user.password) else False

    @with_async_session
    async def update_info(self, user: UserModel, session: AsyncSession | None = None) -> UserModel:
        return await self.users_repository.update(instance=user, session=session)

    @with_async_session
    async def update_avatar(self, user: UserModel, photo: UploadFile, session: AsyncSession | None = None) -> UserModel:
        return await self.users_repository.upload_photo(instance=user, photo=photo, session=session)

    def get_avatar(self, user: UserModel) -> str | None:
        return self.users_repository.download_photo(instance=user)

    def delete_avatar(self, user: UserModel):
        self.users_repository.delete_photo(instance=user)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password) -> str:
        return pwd_context.hash(password)


users_service = UsersService(users_repository=users_repository)
