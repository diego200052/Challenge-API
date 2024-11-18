from core.database import Base
from sqlalchemy import Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from decimal import Decimal


class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    account_name: Mapped[str] = mapped_column(String(512), nullable=False)
    bank_name: Mapped[str] = mapped_column(String(255), nullable=False)
    account_number: Mapped[str] = mapped_column(String(50), nullable=False)
    current_balance: Mapped[Decimal] = mapped_column(Numeric(24, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(20), nullable=False)

    payments = relationship(
        "Payment",
        foreign_keys="Payment.bank_account_id",
        back_populates="account_details",
    )
