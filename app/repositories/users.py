from app.models.users import User as UserModel
from app.repositories.base import BaseRepository
from app.repositories.photo import PhotoRepository


class UsersRepository(BaseRepository, PhotoRepository):
    def __init__(self):
        super().__init__(model=UserModel)


users_repository = UsersRepository()
