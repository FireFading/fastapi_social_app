from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    created_at: datetime
    from_user_id: UUID
    chat_id: UUID
    content: str


class Chat(BaseModel):
    name: str
    private: bool
    active: bool


class ShowChat(BaseModel):
    id: UUID
    name: str
    private: bool
    active: bool
