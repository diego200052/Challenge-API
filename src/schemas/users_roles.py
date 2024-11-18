from pydantic import BaseModel
from typing import Optional
import uuid


class UserRoleBase(BaseModel):
    user_id: uuid.UUID
    role_id: uuid.UUID


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(BaseModel):
    user_id: Optional[uuid.UUID]
    role_id: Optional[uuid.UUID]


class UserRoleSchema(UserRoleBase):
    id: uuid.UUID
    role_name: str
    role_description: Optional[str] = None

    class Config:
        orm_mode = True
