import uuid
from sqlalchemy.orm import Session

from app.models.account import Account, AccountType, AccountStatus
from app.services.balance_service import get_account_balance


def create_account(db: Session, user_id: uuid.UUID, account_type: AccountType, currency: str):
    account = Account(
        user_id=user_id,
        account_type=account_type,
        currency=currency,
        status=AccountStatus.active
    )
    db.add(account)
    db.flush()  # generate account.id

    return account


def get_account_with_balance(db: Session, account_id):
    account = db.get(Account, account_id)
    if not account:
        return None

    balance = get_account_balance(db, account_id)

    return {
        "id": account.id,
        "user_id": account.user_id,
        "type": account.account_type.value,
        "currency": account.currency,
        "status": account.status.value,
        "balance": str(balance),
    }
