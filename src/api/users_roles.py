import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.users_roles import UserRoleSchema, UserRoleCreate, UserRoleUpdate
from models.public.users_roles import UserRole
from models.public.users import User
from models.public.roles import Role

router = APIRouter()


# Endpoint para asignar un rol a un usuario
@router.post("/", response_model=UserRoleSchema, status_code=status.HTTP_201_CREATED)
def create_user_role(user_role: UserRoleCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario y el rol existen
    user = db.query(User).filter(User.id == user_role.user_id).first()
    role = db.query(Role).filter(Role.id == user_role.role_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Verificar si ya existe la asignación de rol para el usuario
    existing_user_role = (
        db.query(UserRole)
        .filter(
            UserRole.user_id == user_role.user_id, UserRole.role_id == user_role.role_id
        )
        .first()
    )
    if existing_user_role:
        raise HTTPException(
            status_code=400, detail="The user already has this role assigned"
        )

    new_user_role = UserRole(
        id=uuid.uuid4(), user_id=user_role.user_id, role_id=user_role.role_id
    )

    db.add(new_user_role)
    db.commit()
    db.refresh(new_user_role)
    return new_user_role


# Endpoint para obtener todos los roles asignados a usuarios
@router.get("/", response_model=List[UserRoleSchema])
def read_user_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_roles = db.query(UserRole).offset(skip).limit(limit).all()
    return user_roles


# Endpoint para obtener un rol asignado específico por ID
@router.get("/{user_role_id}", response_model=UserRoleSchema)
def read_user_role(user_role_id: uuid.UUID, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.id == user_role_id).first()
    if user_role is None:
        raise HTTPException(status_code=404, detail="User role assignment not found")
    return user_role


# Endpoint para actualizar la asignación de un rol a un usuario
@router.put("/{user_role_id}", response_model=UserRoleSchema)
def update_user_role(
    user_role_id: uuid.UUID,
    user_role_update: UserRoleUpdate,
    db: Session = Depends(get_db),
):
    user_role = db.query(UserRole).filter(UserRole.id == user_role_id).first()
    if user_role is None:
        raise HTTPException(status_code=404, detail="User role assignment not found")

    for var, value in vars(user_role_update).items():
        if value is not None:
            setattr(user_role, var, value)

    db.commit()
    db.refresh(user_role)
    return user_role


# Endpoint para eliminar la asignación de un rol a un usuario
@router.delete("/{user_role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_role(user_role_id: uuid.UUID, db: Session = Depends(get_db)):
    user_role = db.query(UserRole).filter(UserRole.id == user_role_id).first()
    if user_role is None:
        raise HTTPException(status_code=404, detail="User role assignment not found")

    db.delete(user_role)
    db.commit()
    return
