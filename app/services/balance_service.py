from sqlalchemy import select, func, case
from sqlalchemy.orm import Session

from app.models.ledger import LedgerEntry, LedgerEntryType


def get_account_balance(db: Session, account_id):
    """
    Calculates balance as:
    SUM(credits) - SUM(debits)
    """

    balance_stmt = (
        select(
            func.coalesce(
                func.sum(
                    case(
                        (LedgerEntry.entry_type == LedgerEntryType.credit, LedgerEntry.amount),
                        (LedgerEntry.entry_type == LedgerEntryType.debit, -LedgerEntry.amount),
                        else_=0,
                    )
                ),
                0,
            )
        )
        .where(LedgerEntry.account_id == account_id)
    )

    balance = db.execute(balance_stmt).scalar_one()
    return balance
