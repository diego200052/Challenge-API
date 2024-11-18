from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
from schemas.users_roles import UserRoleSchema


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


class UserCreate(UserBase):
    password: str
    created_at: Optional[datetime] = None


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]


class UserSchema(UserBase):
    id: uuid.UUID
    created_at: Optional[datetime] = None
    user_roles: List[UserRoleSchema] = []

    class Config:
        orm_mode = True
