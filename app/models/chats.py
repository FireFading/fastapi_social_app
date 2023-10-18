import uuid
from datetime import datetime

from app.database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Chat(Base):
    __tablename__ = "chats"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    name = Column(String(255), nullable=True)
    private = Column(Boolean, default=True, nullable=False)
    active = Column(Boolean, default=True, nullable=False)


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    from_user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    chat_id = Column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    content = Column(String(255), nullable=False)

    read_statuses = relationship("ReadStatus", back_populates="message")


class ReadStatus(Base):
    __tablename__ = "read_statuses"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    read_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message_id = Column(ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)

    message = relationship("Message", back_populates="read_statuses")


class UserChat(Base):
    __tablename__ = "users_chats"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    chat_id = Column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
