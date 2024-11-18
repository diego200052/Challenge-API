import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.payments import PaymentSchema, PaymentCreate, PaymentUpdate
from models.public.payments import Payment
from models.public.bank_accounts import BankAccount
from models.public.expenses import Expense
from models.public.users import User
from datetime import datetime
from core.config import settings

router = APIRouter()


# Endpoint para obtener todos los pagos
@router.get("/", response_model=List[PaymentSchema])
def read_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    payments = db.query(Payment).offset(skip).limit(limit).all()
    return payments


@router.get("/this-month", response_model=List[PaymentSchema])
def get_payments_this_month(db: Session = Depends(get_db)):

    now = datetime.now(settings.timezone_pytz)
    start_date = now.replace(day=1)
    end_date = now

    payments = (
        db.query(Payment)
        .filter(
            Payment.payment_date.between(start_date, end_date),
            Payment.status == 3,  # Payment completed
        )
        .all()
    )

    return payments


# Endpoint para obtener un pago por ID
@router.get("/{payment_id}", response_model=PaymentSchema)
def read_payment(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


# Endpoint para actualizar un pago
@router.put("/{payment_id}", response_model=PaymentSchema)
def update_payment(
    payment_id: uuid.UUID, payment_update: PaymentUpdate, db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    for var, value in vars(payment_update).items():
        if value is not None:
            setattr(payment, var, value)

    db.commit()
    db.refresh(payment)
    return payment


# Endpoint para eliminar un pago
@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    db.delete(payment)
    db.commit()
    return


# Endpoint para aprobar un pago
@router.post("/{payment_id}/approve", response_model=PaymentSchema)
def approve_payment(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    # approver = db.query(User).filter(User.id == approver_id).first()
    # if approver is None:
    #    raise HTTPException(status_code=404, detail="Approver user not found")

    payment.status = 1  # Actualizar el estado a aprobado (1)
    # payment.approved_by = approver_id
    db.commit()
    db.refresh(payment)
    return payment


# Endpoint para cancelar un pago
@router.post("/{payment_id}/cancel", response_model=PaymentSchema)
def cancel_payment(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment.status = 2  # Actualizar el estado a cancelado (2)
    db.commit()
    db.refresh(payment)
    return payment


# Endpoint para ejecutar un pago
@router.post("/{payment_id}/execute", response_model=PaymentSchema)
def execute_payment(
    payment_id: uuid.UUID, executor_id: uuid.UUID, db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    executor = db.query(User).filter(User.id == executor_id).first()
    if executor is None:
        raise HTTPException(status_code=404, detail="Executor user not found")

    # Verificar si el pago ya ha sido ejecutado
    if payment.status == 3:
        raise HTTPException(status_code=400, detail="Payment has already been executed")

    # Verificar si la cuenta bancaria tiene fondos suficientes
    if payment.bank_account_id:
        bank_account = (
            db.query(BankAccount)
            .filter(BankAccount.id == payment.bank_account_id)
            .first()
        )
        if bank_account is None:
            raise HTTPException(status_code=404, detail="Bank account not found")

        if bank_account.current_balance < payment.total_amount:
            raise HTTPException(
                status_code=400,
                detail="Insufficient funds in the associated bank account",
            )

        # Reducir el balance de la cuenta bancaria
        bank_account.current_balance -= payment.total_amount
        db.add(bank_account)

    # Actualizar el estado del pago a ejecutado
    payment.status = 3  # Estado de ejecutado
    payment.executed_by = executor_id
    payment.payment_date = datetime.now(
        settings.timezone_pytz
    )  # Actualizar la fecha de ejecución
    db.commit()
    db.refresh(payment)
    return payment


@router.post("/generate", response_model=List[PaymentSchema])
def generate_payments(payload: PaymentCreate, db: Session = Depends(get_db)):
    # Obtener los IDs de los gastos desde el payload
    expense_ids = payload.expense_ids

    # Consultar los gastos aprobados
    expenses = (
        db.query(Expense).filter(Expense.id.in_(expense_ids), Expense.status == 1).all()
    )
    if not expenses:
        raise HTTPException(
            status_code=404, detail="No approved expenses found for the given IDs."
        )

    # Validar que todos los gastos se encontraron y están aprobados
    if len(expenses) != len(expense_ids):
        raise HTTPException(
            status_code=400, detail="Some expenses are missing or not approved."
        )

    # Calcular el monto total y generar pagos
    payments = []
    for expense in expenses:

        new_payment = Payment(
            id=uuid.uuid4(),
            payment_date=datetime.now(settings.timezone_pytz),
            total_amount=expense.total_cost,  # Usar el total_cost del gasto
            status=0,  # Estado inicial: Pending
            created_by=payload.created_by,  # Usar el created_by enviado
        )
        db.add(new_payment)
        db.flush()  # Obtener el ID del nuevo pago para asociarlo al gasto

        # Asociar el pago al gasto
        expense.payment_id = new_payment.id
        db.add(expense)

        # Agregar el pago a la lista de respuesta
        payments.append(new_payment)

    db.commit()

    return payments
