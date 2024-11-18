import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.bank_accounts import (
    BankAccountSchema,
    BankAccountCreate,
    BankAccountUpdate,
)
from models.public.bank_accounts import BankAccount
from decimal import Decimal

router = APIRouter()


# Endpoint para crear una nueva cuenta bancaria
@router.post("/", response_model=BankAccountSchema, status_code=status.HTTP_201_CREATED)
def create_bank_account(bank_account: BankAccountCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe una cuenta bancaria con el mismo número de cuenta
    existing_account = (
        db.query(BankAccount)
        .filter(BankAccount.account_number == bank_account.account_number)
        .first()
    )
    if existing_account:
        raise HTTPException(
            status_code=400, detail="La cuenta bancaria ya está registrada"
        )

    new_bank_account = BankAccount(
        id=uuid.uuid4(),
        account_name=bank_account.account_name,
        bank_name=bank_account.bank_name,
        account_number=bank_account.account_number,
        current_balance=bank_account.current_balance,
        currency=bank_account.currency,
    )
    db.add(new_bank_account)
    db.commit()
    db.refresh(new_bank_account)
    return new_bank_account


# Endpoint para obtener todas las cuentas bancarias
@router.get("/", response_model=List[BankAccountSchema])
def read_bank_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bank_accounts = db.query(BankAccount).offset(skip).limit(limit).all()
    return bank_accounts


# Endpoint para obtener una cuenta bancaria por ID
@router.get("/{bank_account_id}", response_model=BankAccountSchema)
def read_bank_account(bank_account_id: uuid.UUID, db: Session = Depends(get_db)):
    bank_account = (
        db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    )
    if bank_account is None:
        raise HTTPException(status_code=404, detail="Cuenta bancaria no encontrada")
    return bank_account


# Endpoint para actualizar una cuenta bancaria
@router.put("/{bank_account_id}", response_model=BankAccountSchema)
def update_bank_account(
    bank_account_id: uuid.UUID,
    bank_account_update: BankAccountUpdate,
    db: Session = Depends(get_db),
):
    bank_account = (
        db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    )
    if bank_account is None:
        raise HTTPException(status_code=404, detail="Cuenta bancaria no encontrada")
    for var, value in vars(bank_account_update).items():
        if value is not None:
            setattr(bank_account, var, value)
    db.commit()
    db.refresh(bank_account)
    return bank_account


# Endpoint para eliminar una cuenta bancaria
@router.delete("/{bank_account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bank_account(bank_account_id: uuid.UUID, db: Session = Depends(get_db)):
    bank_account = (
        db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    )
    if bank_account is None:
        raise HTTPException(status_code=404, detail="Cuenta bancaria no encontrada")
    db.delete(bank_account)
    db.commit()
    return


@router.post(
    "/{bank_account_id}/deduct-balance",
    response_model=BankAccountSchema,
    status_code=status.HTTP_200_OK,
)
def deduct_balance(
    bank_account_id: uuid.UUID, amount: Decimal, db: Session = Depends(get_db)
):
    """
    Endpoint para descontar saldo de una cuenta bancaria.

    Args:
    - bank_account_id: ID de la cuenta bancaria.
    - amount: Monto a descontar.
    """
    # Buscar la cuenta bancaria
    bank_account = (
        db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    )
    if not bank_account:
        raise HTTPException(status_code=404, detail="Cuenta bancaria no encontrada")

    # Verificar que el monto a descontar sea válido
    if amount <= 0:
        raise HTTPException(
            status_code=400, detail="El monto a descontar debe ser mayor a 0"
        )

    # Verificar si hay fondos suficientes
    if bank_account.current_balance < amount:
        raise HTTPException(
            status_code=400, detail="Fondos insuficientes en la cuenta bancaria"
        )

    # Descontar el saldo
    bank_account.current_balance -= amount
    db.commit()
    db.refresh(bank_account)

    return bank_account
