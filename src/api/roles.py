import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.roles import RoleSchema, RoleCreate, RoleUpdate
from models.public.roles import Role

router = APIRouter()


# Endpoint para crear un nuevo rol
@router.post("/", response_model=RoleSchema, status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    # Verificar si el rol con el mismo nombre ya existe
    existing_role = db.query(Role).filter(Role.name == role.name).first()
    if existing_role:
        raise HTTPException(
            status_code=400, detail="Role with this name already exists"
        )

    new_role = Role(id=uuid.uuid4(), name=role.name, description=role.description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


# Endpoint para obtener todos los roles
@router.get("/", response_model=List[RoleSchema])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles


# Endpoint para obtener un rol por ID
@router.get("/{role_id}", response_model=RoleSchema)
def read_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


# Endpoint para actualizar un rol
@router.put("/{role_id}", response_model=RoleSchema)
def update_role(
    role_id: uuid.UUID, role_update: RoleUpdate, db: Session = Depends(get_db)
):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")

    for var, value in vars(role_update).items():
        if value is not None:
            setattr(role, var, value)

    db.commit()
    db.refresh(role)
    return role


# Endpoint para eliminar un rol
@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")

    db.delete(role)
    db.commit()
    return
