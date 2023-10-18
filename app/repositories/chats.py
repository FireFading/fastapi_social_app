from app.models.chats import Chat as ChatModel
from app.models.chats import Message as MessageModel
from app.models.chats import ReadStatus as ReadStatusModel
from app.models.chats import UserChat as UserChatModel
from app.repositories.base import BaseRepository


class ChatsRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=ChatModel)


class MessagesRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=MessageModel)


class UsersChatsRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=UserChatModel)


class ReadStatusesRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=ReadStatusModel)


chats_repository = ChatsRepository()
messages_repository = MessagesRepository()
users_chats_repository = UsersChatsRepository()
read_statuses_repository = ReadStatusesRepository()
