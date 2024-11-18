import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.users import UserSchema, UserCreate, UserUpdate
from models.public.users import User
from datetime import datetime
from core.config import settings

router = APIRouter()


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        id=uuid.uuid4(),
        username=user.username,
        email=user.email,
        password=user.password,
        created_at=user.created_at or datetime.now(settings.timezone),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    users = db.query(User).offset(skip).limit(limit).all()

    return users


@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: uuid.UUID, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: uuid.UUID, user_update: UserUpdate, db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for var, value in vars(user_update).items():
        if value is not None:
            setattr(user, var, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return
