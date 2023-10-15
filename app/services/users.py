from app.models.users import User as UserModel
from app.repositories.users import UsersRepository, users_repository
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersService:
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    async def get_user(self, session: AsyncSession, **kwargs) -> UserModel | None:
        return await self.users_repository.get(session=session, **kwargs)

    async def create(self, user: UserModel, session: AsyncSession) -> UserModel:
        user.password = self.get_password_hash(user.password)
        return await self.users_repository.create(instance=user, session=session)

    async def authenticate_user(self, username: str, password: str, session: AsyncSession) -> bool:
        user = await self.users_repository.get(session=session, username=username)
        if not user:
            return False
        return user if self.verify_password(plain_password=password, hashed_password=user.password) else False

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password) -> str:
        return pwd_context.hash(password)


users_service = UsersService(users_repository=users_repository)
