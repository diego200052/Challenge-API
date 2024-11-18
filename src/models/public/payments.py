from core.database import Base
from sqlalchemy import TIMESTAMP, Numeric, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from decimal import Decimal
from datetime import date


class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    payment_date: Mapped[date] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=True
    )
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    bank_account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("bank_accounts.id"), name="bank_account_id_fk", nullable=True
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), name="created_by_fk", nullable=False
    )
    approved_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), name="approved_by_fk", nullable=True
    )
    executed_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), name="executed_by_fk", nullable=True
    )

    account_details = relationship(
        "BankAccount", foreign_keys=[bank_account_id], back_populates="payments"
    )
    creator = relationship(
        "User", foreign_keys=[created_by], back_populates="created_payments"
    )
    approver = relationship(
        "User", foreign_keys=[approved_by], back_populates="approved_payments"
    )
    executor = relationship(
        "User", foreign_keys=[executed_by], back_populates="executed_payments"
    )
    expenses_payment = relationship(
        "Expense", foreign_keys="Expense.payment_id", back_populates="payment"
    )
