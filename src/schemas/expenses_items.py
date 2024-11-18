from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
import uuid


class ExpenseItemBase(BaseModel):
    item_name: str
    description: Optional[str]
    cost: Decimal


class ExpenseItemCreate(ExpenseItemBase):
    pass


class ExpenseItemUpdate(BaseModel):
    item_name: Optional[str]
    description: Optional[str]
    cost: Optional[Decimal]


class ExpenseItemSchema(ExpenseItemBase):
    id: uuid.UUID
    expense_id: uuid.UUID

    class Config:
        orm_mode = True
