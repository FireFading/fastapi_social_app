from uuid import UUID

from app.database import with_async_session
from app.models.chats import Chat as ChatModel
from app.models.chats import Message as MessageModel
from app.models.chats import ReadStatus as ReadStatusModel
from app.models.chats import UserChat as UserChatModel
from app.repositories.chats import (
    ChatsRepository,
    MessagesRepository,
    ReadStatusesRepository,
    UsersChatsRepository,
    chats_repository,
    messages_repository,
    read_statuses_repository,
    users_chats_repository,
)
from sqlalchemy.ext.asyncio import AsyncSession


class ChatsService:
    def __init__(
        self,
        chats_repository: ChatsRepository,
        messages_repository: MessagesRepository,
        users_chats_repository: UsersChatsRepository,
        read_statuses_repository: ReadStatusesRepository,
    ) -> None:
        self.chats_repository = chats_repository
        self.messages_repository = messages_repository
        self.users_chats_repository = users_chats_repository
        self.read_statuses_repository = read_statuses_repository

    @with_async_session
    async def get_chats(self, session: AsyncSession | None = None, **kwargs) -> ChatModel:
        chats_ids = [
            user_chat.chat_id for user_chat in await self.users_chats_repository.filter(session=session, **kwargs)
        ]
        return await self.chats_repository.filter(session=session, id__in=chats_ids)

    @with_async_session
    async def get_members(self, chat_id: UUID, session: AsyncSession | None = None) -> list[UUID]:
        chat_users = await self.users_chats_repository.filter(session=session, chat_id=chat_id)
        return [chat_user.user_id for chat_user in chat_users]

    @with_async_session
    async def get_messages(self, chat_id: UUID, session: AsyncSession | None = None) -> list[MessageModel]:
        return await self.messages_repository.filter(session=session, chat_id=chat_id)

    @with_async_session
    async def send_message(self, message: MessageModel, session: AsyncSession | None = None) -> MessageModel:
        return await self.messages_repository.create(instance=message, session=session)

    @with_async_session
    async def add_read_status(
        self, read_status: ReadStatusModel, session: AsyncSession | None = None
    ) -> ReadStatusModel:
        return await self.read_statuses_repository.create(instance=read_status, session=session)

    @with_async_session
    async def create_chat(self, chat: ChatModel, session: AsyncSession | None = None) -> ChatModel:
        return await self.chats_repository.create(instance=chat, session=session)

    @with_async_session
    async def add_member(self, user_chat: UserChatModel, session: AsyncSession | None = None):
        await self.users_chats_repository.create(instance=user_chat, session=session)

    @with_async_session
    async def remove_member(self, user_chat: UserChatModel, session: AsyncSession | None = None):
        await self.users_chats_repository.delete(instance=user_chat, session=session)


chats_service = ChatsService(
    chats_repository=chats_repository,
    messages_repository=messages_repository,
    users_chats_repository=users_chats_repository,
    read_statuses_repository=read_statuses_repository,
)
