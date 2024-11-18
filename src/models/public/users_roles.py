from core.database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid


class UserRole(Base):
    __tablename__ = "users_roles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), name="user_id_fk", nullable=False
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id"), name="role_id_fk", nullable=False
    )

    # Restricción para que la combinación de user_id y role_id sea única
    __table_args__ = (
        UniqueConstraint("user_id_fk", "role_id_fk", name="uix_user_role"),
    )

    # Propiedades para acceder a los datos relacionados del Role
    role_name = property(lambda self: self.role.name)
    role_description = property(lambda self: self.role.description)

    # Relaciones con User y Role para establecer la asociación bidireccional
    user = relationship("User", foreign_keys=[user_id], back_populates="user_roles")
    role = relationship("Role", foreign_keys=[role_id], back_populates="user_roles")
