import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.expenses import ExpenseSchema, ExpenseCreate, ExpenseUpdate
from schemas.payments import PaymentSchema
from models.public.expenses import Expense
from models.public.payments import Payment
from models.public.users import User
from datetime import datetime
from core.config import settings

router = APIRouter()


# Endpoint para crear un nuevo gasto
@router.post("/", response_model=ExpenseSchema, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    # Verificar si el proveedor existe, si se especifica
    # if expense.provider_id:
    #    provider = db.query(Provider).filter(Provider.id == expense.provider_id).first()
    #    if provider is None:
    #        raise HTTPException(status_code=404, detail="Provider not found")

    # Verificar si el creador del gasto existe
    creator = db.query(User).filter(User.id == expense.created_by).first()
    if creator is None:
        raise HTTPException(status_code=404, detail="Creator user not found")

    # Verificar si el aprobador del gasto existe, si fue especificado
    # if expense.approved_by:
    #    approver = db.query(User).filter(User.id == expense.approved_by).first()
    #    if approver is None:
    #        raise HTTPException(status_code=404, detail="Approver user not found")

    new_expense = Expense(
        id=uuid.uuid4(),
        expense_date=expense.expense_date or datetime.now(settings.timezone_pytz),
        description=expense.description,
        due_date=expense.due_date,
        total_cost=expense.total_cost,
        recipient_account=expense.recipient_account,
        status=expense.status,
        provider_id=expense.provider_id,
        created_by=expense.created_by,
        approved_by=expense.approved_by,
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


# Endpoint para obtener todos los gastos
@router.get("/", response_model=List[ExpenseSchema])
def read_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    expenses = db.query(Expense).offset(skip).limit(limit).all()
    return expenses


@router.get("/this-month", response_model=List[ExpenseSchema])
def get_expenses_last_month(db: Session = Depends(get_db)):

    now = datetime.now(settings.timezone_pytz)
    start_date = now.replace(day=1)
    end_date = now

    expenses = (
        db.query(Expense)
        .filter(
            Expense.expense_date.between(start_date, end_date),
            Expense.status == 1,  # Aprovved
        )
        .all()
    )

    return expenses


# Endpoint para obtener un gasto por ID
@router.get("/{expense_id}", response_model=ExpenseSchema)
def read_expense(expense_id: uuid.UUID, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


# Endpoint para actualizar un gasto
@router.put("/{expense_id}", response_model=ExpenseSchema)
def update_expense(
    expense_id: uuid.UUID, expense_update: ExpenseUpdate, db: Session = Depends(get_db)
):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    for var, value in vars(expense_update).items():
        if value is not None:
            setattr(expense, var, value)

    db.commit()
    db.refresh(expense)
    return expense


# Endpoint para eliminar un gasto
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: uuid.UUID, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return


# Endpoint para aprobar un gasto
@router.post("/{expense_id}/approve", response_model=ExpenseSchema)
def approve_expense(
    expense_id: uuid.UUID, db: Session = Depends(get_db)
):  # , approver_id: uuid.UUID
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    # approver = db.query(User).filter(User.id == approver_id).first()
    # if approver is None:
    #    raise HTTPException(status_code=404, detail="Approver user not found")

    expense.status = 1  # Actualizar el estado a aprobado (1)
    # expense.approved_by = approver_id
    db.commit()
    db.refresh(expense)
    return expense


# Endpoint para cancelar un gasto
@router.post("/{expense_id}/cancel", response_model=ExpenseSchema)
def cancel_expense(expense_id: uuid.UUID, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.status = 2  # Actualizar el estado a cancelado (2)
    db.commit()
    db.refresh(expense)
    return expense


# Endpoint para generar un pago para un gasto
@router.post("/{expense_id}/generate-payment", response_model=PaymentSchema)
def generate_payment_for_expense(expense_id: uuid.UUID, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    # Verificar si el gasto ya tiene un pago asociado
    if expense.payment_id is not None:
        raise HTTPException(
            status_code=400, detail="Payment already generated for this expense"
        )

    # Crear un nuevo pago para el gasto
    new_payment = Payment(
        id=uuid.uuid4(),
        payment_date=datetime.now(settings.timezone_pytz),
        total_amount=expense.total_cost,
        status=0,  # Estado inicial para el pago (0 = pendiente)
        bank_account_id=None,  # Puede ser especificado según la lógica de negocio
        created_by=expense.created_by,
        approved_by=None,
        executed_by=None,
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    # Asociar el pago al gasto
    expense.payment_id = new_payment.id
    db.commit()
    db.refresh(expense)

    return new_payment
