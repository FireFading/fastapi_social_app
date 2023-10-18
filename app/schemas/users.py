from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserCreate(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    password: str | None = None


class UserShow(BaseModel):
    id: UUID
    username: str
    email: str | None = None
    full_name: str | None = None


class UserUpdate(BaseModel):
    email: str | None = None
    full_name: str | None


class UserInDB(User):
    hashed_password: str


class UserMember(BaseModel):
    id: UUID


class UpdatePassword(BaseModel):
    old_password: str
    password: str
    new_password: str
