from pydantic import BaseModel
from typing import Optional
import uuid


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]


class RoleSchema(RoleBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
