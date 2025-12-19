import uuid
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.transaction_service import deposit, withdraw, transfer

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/deposit")
def deposit_money(
    account_id: uuid.UUID,
    amount: Decimal,
    currency: str,
    description: str | None = None,
    db: Session = Depends(get_db),
):
    try:
        tx = deposit(db, account_id, amount, currency, description)
        return {"transaction_id": tx.id, "status": tx.status.value}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/withdraw")
def withdraw_money(
    account_id: uuid.UUID,
    amount: Decimal,
    currency: str,
    description: str | None = None,
    db: Session = Depends(get_db),
):
    try:
        tx = withdraw(db, account_id, amount, currency, description)
        return {"transaction_id": tx.id, "status": tx.status.value}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/transfer")
def transfer_money(
    source_account_id: uuid.UUID,
    destination_account_id: uuid.UUID,
    amount: Decimal,
    currency: str,
    description: str | None = None,
    db: Session = Depends(get_db),
):
    try:
        tx = transfer(
            db,
            source_account_id,
            destination_account_id,
            amount,
            currency,
            description,
        )
        return {"transaction_id": tx.id, "status": tx.status.value}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
