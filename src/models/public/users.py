from core.database import Base
from sqlalchemy import TIMESTAMP, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from datetime import date


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True, server_default=func.now()
    )

    user_roles = relationship(
        "UserRole", back_populates="user", foreign_keys="UserRole.user_id"
    )
    created_expenses = relationship(
        "Expense", back_populates="creator", foreign_keys="Expense.created_by"
    )
    approved_expenses = relationship(
        "Expense", back_populates="approver", foreign_keys="Expense.approved_by"
    )
    created_payments = relationship(
        "Payment", back_populates="creator", foreign_keys="Payment.created_by"
    )
    approved_payments = relationship(
        "Payment", back_populates="approver", foreign_keys="Payment.approved_by"
    )
    executed_payments = relationship(
        "Payment", back_populates="executor", foreign_keys="Payment.executed_by"
    )
