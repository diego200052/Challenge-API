from core.database import Base
from sqlalchemy import Numeric, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from decimal import Decimal


class ExpenseItem(Base):
    __tablename__ = "expenses_items"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    expense_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("expenses.id"), name="expense_id", nullable=False
    )
    item_name: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)

    expense = relationship("Expense", foreign_keys=[expense_id], back_populates="items")
