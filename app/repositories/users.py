from app.models.users import User as UserModel
from app.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=UserModel)


users_repository = UsersRepository()
