from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
import uuid
from schemas.expenses_items import ExpenseItemCreate, ExpenseItemSchema


class ExpenseBase(BaseModel):
    expense_date: Optional[datetime] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    total_cost: Decimal
    recipient_account: Optional[str] = None
    status: int
    payment_id: Optional[uuid.UUID] = None
    provider_id: Optional[uuid.UUID] = None
    created_by: uuid.UUID
    approved_by: Optional[uuid.UUID] = None


class ExpenseCreate(ExpenseBase):
    items: Optional[List[ExpenseItemCreate]] = None


class ExpenseUpdate(BaseModel):
    expense_date: Optional[datetime]
    description: Optional[str]
    due_date: Optional[datetime]
    total_cost: Optional[Decimal]
    recipient_account: Optional[str]
    status: Optional[int]
    provider_id: Optional[uuid.UUID]
    approved_by: Optional[uuid.UUID]
    items: Optional[List[ExpenseItemCreate]]


class ExpenseSchema(ExpenseBase):
    id: uuid.UUID
    items: List[ExpenseItemSchema]

    class Config:
        orm_mode = True
