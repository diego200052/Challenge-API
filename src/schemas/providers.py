from pydantic import BaseModel
from typing import Optional
import uuid


class ProviderBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class ProviderCreate(ProviderBase):
    pass


class ProviderUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]


class ProviderSchema(ProviderBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
