from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
import uuid


class BankAccountBase(BaseModel):
    account_name: str
    bank_name: str
    account_number: str
    current_balance: Decimal
    currency: str


class BankAccountCreate(BankAccountBase):
    pass


class BankAccountUpdate(BaseModel):
    account_name: Optional[str]
    bank_name: Optional[str]
    account_number: Optional[str]
    current_balance: Optional[Decimal]
    currency: Optional[str]


class BankAccountSchema(BankAccountBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
