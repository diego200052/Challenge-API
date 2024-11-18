from core.database import Base
from sqlalchemy import TIMESTAMP, Numeric, ForeignKey, String, Integer, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from decimal import Decimal
from datetime import date


class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    expense_date: Mapped[date] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    due_date: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    total_cost: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    recipient_account: Mapped[str] = mapped_column(String(50), nullable=True)
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    provider_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("providers.id"), name="provider_id_fk", nullable=True
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), name="created_by_fk", nullable=False
    )
    approved_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), name="approved_by_fk", nullable=True
    )
    payment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("payments.id"), name="payment_fk", nullable=True
    )

    provider = relationship(
        "Provider", foreign_keys=[provider_id], back_populates="expenses"
    )
    creator = relationship(
        "User", foreign_keys=[created_by], back_populates="created_expenses"
    )
    approver = relationship(
        "User", foreign_keys=[approved_by], back_populates="approved_expenses"
    )
    payment = relationship(
        "Payment", foreign_keys=[payment_id], back_populates="expenses_payment"
    )
    items = relationship(
        "ExpenseItem", foreign_keys="ExpenseItem.expense_id", back_populates="expense"
    )
