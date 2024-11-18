from core.database import Base
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=True)

    user_roles = relationship(
        "UserRole", back_populates="role", foreign_keys="UserRole.role_id"
    )
