from uuid import UUID

from app.config import oauth2_scheme
from app.controllers.chats import chats_controller
from app.controllers.users import users_controller
from app.schemas.chats import Chat as ChatSchema
from app.schemas.chats import Message as MessageSchema
from app.schemas.chats import ShowChat as ShowChatSchema
from app.schemas.users import UserMember as UserMemberSchema
from fastapi import APIRouter, Depends, WebSocket, status

router = APIRouter(prefix="/chats", tags=["chats"], responses={404: {"description": "Not found"}})


@router.get("/all/", response_model=list[ShowChatSchema])
async def get_chats(token: str = Depends(oauth2_scheme)):
    current_user = await users_controller.verify_token(token=token)
    return await chats_controller.get_chats(user=current_user)


@router.post(
    "/new/",
    response_model=ChatSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create chat",
)
async def create_chat(
    chat_schema: ChatSchema,
    token: str = Depends(oauth2_scheme),
):
    user = await users_controller.verify_token(token=token)
    return await chats_controller.create_chat(user=user, chat_schema=chat_schema)


@router.get(
    "/{chat_id}/messages/",
    response_model=list[MessageSchema],
    status_code=status.HTTP_200_OK,
    summary="Get messages for chat",
)
async def get_messages(
    chat_id: UUID,
    token: str = Depends(oauth2_scheme),
):
    current_user = await users_controller.verify_token(token=token)
    return await chats_controller.get_messages(user=current_user, chat_id=chat_id)


@router.post(
    "/{chat_id}/add-member/",
    response_model=list[UserMemberSchema],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Add member to chat",
)
async def add_member(chat_id: UUID, member: UserMemberSchema, token: str = Depends(oauth2_scheme)):
    user = await users_controller.verify_token(token=token)
    await chats_controller.add_member(chat_id=chat_id, member=member, user=user)
    return await chats_controller.get_members(chat_id=chat_id, user=user)


@router.get(
    "/{chat_id}/members/",
    response_model=list[UserMemberSchema],
    status_code=status.HTTP_200_OK,
    summary="Get chat members",
)
async def members(chat_id: UUID, token: str = Depends(oauth2_scheme)):
    user = await users_controller.verify_token(token=token)
    return await chats_controller.get_members(chat_id=chat_id, user=user)


@router.websocket("/{chat_id}/")
async def chatting(
    websocket: WebSocket,
    chat_id: UUID,
    message_schema: MessageSchema,
    token: str = Depends(oauth2_scheme),
):
    user = await users_controller.verify_token(token=token)
    await chats_controller.check_allowed_user(user=user, chat_id=chat_id)
    await chats_controller.connect(websocket=websocket, user=user)
    while True:
        data = await websocket.receive_text()
        await chats_controller.send_message(data=data, chat_id=chat_id, user=user, message_schema=message_schema)
