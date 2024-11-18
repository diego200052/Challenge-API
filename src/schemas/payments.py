from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
import uuid


class PaymentBase(BaseModel):
    payment_date: Optional[datetime] = None
    total_amount: Decimal
    status: int
    bank_account_id: Optional[uuid.UUID] = None
    created_by: uuid.UUID
    approved_by: Optional[uuid.UUID] = None
    executed_by: Optional[uuid.UUID] = None


class PaymentCreate(BaseModel):
    payment_date: Optional[datetime] = None
    total_amount: Optional[Decimal] = 0
    status: Optional[int] = 0
    bank_account_id: Optional[uuid.UUID] = None
    created_by: uuid.UUID
    approved_by: Optional[uuid.UUID] = None
    executed_by: Optional[uuid.UUID] = None
    expense_ids: List[uuid.UUID]


class PaymentUpdate(BaseModel):
    payment_date: Optional[datetime]
    total_amount: Optional[Decimal]
    status: Optional[int]
    bank_account_id: Optional[uuid.UUID]
    approved_by: Optional[uuid.UUID]
    executed_by: Optional[uuid.UUID]
    expense_ids: Optional[List[uuid.UUID]]


class PaymentSchema(BaseModel):
    id: uuid.UUID
    payment_date: Optional[datetime]
    total_amount: Decimal
    status: int
    bank_account_id: Optional[uuid.UUID]
    created_by: uuid.UUID
    approved_by: Optional[uuid.UUID]
    executed_by: Optional[uuid.UUID]

    class Config:
        orm_mode = True
