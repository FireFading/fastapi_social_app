from uuid import UUID

from app.exceptions.chats import NotAllowedException
from app.models.chats import Chat as ChatModel
from app.models.chats import Message as MessageModel
from app.models.chats import UserChat as UserChatModel
from app.models.users import User as UserModel
from app.schemas.chats import Chat as ChatSchema
from app.services.chats import ChatsService, chats_service


class ChatsController:
    def __init__(self, chats_service: ChatsService) -> None:
        self.chats_service = chats_service

    async def check_allowed_user(self, user: UserModel, chat_id: UUID) -> bool:
        user_ids = await self.chats_service.get_members(chat_id=chat_id)
        return user.id in user_ids

    async def get_chats(self, user: UserModel) -> list[ChatModel]:
        return await self.chats_service.get_chats(user_id=user.id)

    async def create_chat(self, user: UserModel, chat_schema: ChatSchema) -> ChatModel:
        chat = ChatModel(**chat_schema.model_dump())
        created_chat = await self.chats_service.create_chat(chat=chat)
        user_chat = UserChatModel(user_id=user.id, chat_id=created_chat.id)
        await self.chats_service.add_member(user_chat=user_chat)
        return created_chat

    async def get_messages(self, user: UserModel, chat_id: UUID) -> list[MessageModel]:
        if not await self.check_allowed_user(user=user, chat_id=chat_id):
            raise NotAllowedException()
        return await self.chats_service.get_messages(chat_id=chat_id)


chats_controller = ChatsController(chats_service=chats_service)
