import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account, AccountType
from app.services.account_service import create_account, get_account_with_balance
from app.services.balance_service import get_account_balance
from app.models.ledger import LedgerEntry

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_new_account(
    user_id: uuid.UUID,
    account_type: AccountType,
    currency: str,
    db: Session = Depends(get_db),
):
    account = create_account(db, user_id, account_type, currency)
    return {"id": account.id}


@router.get("/{account_id}")
def get_account(account_id: uuid.UUID, db: Session = Depends(get_db)):
    account = get_account_with_balance(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.get("/{account_id}/ledger")
def get_account_ledger(account_id: uuid.UUID, db: Session = Depends(get_db)):
    entries = (
        db.query(LedgerEntry)
        .filter(LedgerEntry.account_id == account_id)
        .order_by(LedgerEntry.created_at)
        .all()
    )

    return [
        {
            "id": e.id,
            "transaction_id": e.transaction_id,
            "type": e.entry_type.value,
            "amount": str(e.amount),
            "timestamp": e.created_at,
        }
        for e in entries
    ]
