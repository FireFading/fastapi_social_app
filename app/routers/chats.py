from uuid import UUID

from app.config import oauth2_scheme
from app.controllers.chats import chats_controller
from app.controllers.users import users_controller
from app.schemas.chats import Chat as ChatSchema
from app.schemas.chats import Message as MessageSchema
from app.schemas.chats import ShowChat as ShowChatSchema
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/chats", tags=["chats"], responses={404: {"description": "Not found"}})


@router.get("/{chat_id}/messages/", response_model=list[MessageSchema])
async def get_messages(
    chat_id: UUID,
    token: str = Depends(oauth2_scheme),
):
    current_user = await users_controller.verify_token(token=token)
    return await chats_controller.get_messages(user=current_user, chat_id=chat_id)


@router.get("/all/", response_model=list[ShowChatSchema])
async def get_chats(token: str = Depends(oauth2_scheme)):
    current_user = await users_controller.verify_token(token=token)
    return await chats_controller.get_chats(user=current_user)


@router.post("/new/", response_model=ChatSchema, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_schema: ChatSchema,
    token: str = Depends(oauth2_scheme),
):
    user = await users_controller.verify_token(token=token)
    return await chats_controller.create_chat(user=user, chat_schema=chat_schema)
