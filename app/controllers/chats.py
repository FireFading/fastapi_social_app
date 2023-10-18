import contextlib
from uuid import UUID

from app.exceptions.chats import NotAllowedException
from app.models.chats import Chat as ChatModel
from app.models.chats import Message as MessageModel
from app.models.chats import ReadStatus as ReadStatusModel
from app.models.chats import UserChat as UserChatModel
from app.models.users import User as UserModel
from app.schemas.chats import Chat as ChatSchema
from app.schemas.chats import Message as MessageSchema
from app.schemas.users import UserMember as UserMemberSchema
from app.services.chats import ChatsService, chats_service
from fastapi import WebSocket
from websockets.exceptions import ConnectionClosedOK


class ChatsController:
    def __init__(self, chats_service: ChatsService) -> None:
        self.chats_service = chats_service
        self.connection_dict = {}

    async def check_allowed_user(self, user: UserModel, chat_id: UUID) -> bool:
        user_ids = await self.chats_service.get_members(chat_id=chat_id)
        return user.id in user_ids

    async def add_member(self, chat_id: UUID, user: UserModel, member: UserMemberSchema):
        if not await self.check_allowed_user(user=user, chat_id=chat_id):
            raise NotAllowedException()
        user_chat = UserChatModel(user_id=member.id, chat_id=chat_id)
        await self.chats_service.add_member(user_chat=user_chat)

    async def get_members(self, user: UserModel, chat_id: UUID) -> list[UserMemberSchema]:
        if not await self.check_allowed_user(user=user, chat_id=chat_id):
            raise NotAllowedException()
        return await self.chats_service.get_members(chat_id=chat_id)

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

    async def connect(self, user: UserModel, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connection_dict[user.id] = websocket

    def disconnect(self, websocket: WebSocket) -> None:
        self.connection_dict.pop(websocket)

    async def mark_as_read(self, user: UserModel, message_id: UUID) -> None:
        read_status = ReadStatusModel(user_id=user.id, message_id=message_id)
        await self.chats_service.add_read_status(read_status=read_status)

    async def send_message(self, chat_id: UUID, user: UserModel, message_schema: MessageSchema) -> None:
        if not await self.check_allowed_user(user=user, chat_id=chat_id):
            raise NotAllowedException()
        create_message = MessageModel(content=message_schema.content, from_user_id=user.id, chat_id=chat_id)
        message = await self.chats_service.send_message(message=create_message, chat_id=chat_id)
        user_ids = await self.chats_service.get_members(chat_id=chat_id)
        for idx in user_ids:
            if websocket := self.connection_dict.get(idx):
                with contextlib.suppress(ConnectionClosedOK):
                    await websocket.send_text(message.content)
                    await self.mark_as_read(user=user, message_id=message.id)


chats_controller = ChatsController(chats_service=chats_service)
