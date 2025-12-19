from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.transaction import Transaction, TransactionType, TransactionStatus
from app.models.ledger import LedgerEntry, LedgerEntryType
from app.models.account import Account, AccountStatus
from app.services.balance_service import get_account_balance


def deposit(
    db: Session,
    account_id,
    amount: Decimal,
    currency: str,
    description: str | None = None,
):
    """
    Creates a deposit:
    - 1 Transaction (type=deposit)
    - 1 credit LedgerEntry to the destination account
    """
    account = db.get(Account, account_id)
    if not account:
        raise ValueError("Account not found")

    if account.status != AccountStatus.active:
        raise ValueError("Account is not active")

    if account.currency != currency:
        raise ValueError("Currency mismatch")

    tx = Transaction(
        type=TransactionType.deposit,
        destination_account_id=account_id,
        amount=amount,
        currency=currency,
        status=TransactionStatus.pending,
        description=description,
    )
    db.add(tx)
    db.flush()  # get tx.id

    ledger_entry = LedgerEntry(
        account_id=account_id,
        transaction_id=tx.id,
        entry_type=LedgerEntryType.credit,
        amount=amount,
    )
    db.add(ledger_entry)

    tx.status = TransactionStatus.completed
    return tx


def withdraw(
    db: Session,
    account_id,
    amount: Decimal,
    currency: str,
    description: str | None = None,
):
    """
    Creates a withdrawal:
    - Locks the account row
    - Ensures balance will not go negative
    - 1 Transaction (type=withdrawal)
    - 1 debit LedgerEntry from the source account
    """
    account = (
        db.query(Account)
        .filter(Account.id == account_id)
        .with_for_update()
        .one_or_none()
    )

    if not account:
        raise ValueError("Account not found")

    if account.status != AccountStatus.active:
        raise ValueError("Account is not active")

    if account.currency != currency:
        raise ValueError("Currency mismatch")

    balance = get_account_balance(db, account_id)
    if balance < amount:
        raise ValueError("Insufficient funds")

    tx = Transaction(
        type=TransactionType.withdrawal,
        source_account_id=account_id,
        amount=amount,
        currency=currency,
        status=TransactionStatus.pending,
        description=description,
    )
    db.add(tx)
    db.flush()

    ledger_entry = LedgerEntry(
        account_id=account_id,
        transaction_id=tx.id,
        entry_type=LedgerEntryType.debit,
        amount=amount,
    )
    db.add(ledger_entry)

    tx.status = TransactionStatus.completed
    return tx


def transfer(
    db: Session,
    source_account_id,
    destination_account_id,
    amount: Decimal,
    currency: str,
    description: str | None = None,
):
    """
    Creates a transfer:
    - Locks both source and destination accounts
    - Checks source balance (no negative allowed)
    - 1 Transaction (type=transfer)
    - 2 LedgerEntries:
        - debit from source
        - credit to destination
    """
    source = (
        db.query(Account)
        .filter(Account.id == source_account_id)
        .with_for_update()
        .one_or_none()
    )

    dest = (
        db.query(Account)
        .filter(Account.id == destination_account_id)
        .with_for_update()
        .one_or_none()
    )

    if not source or not dest:
        raise ValueError("Account not found")

    if source.status != AccountStatus.active or dest.status != AccountStatus.active:
        raise ValueError("Account not active")

    if source.currency != currency or dest.currency != currency:
        raise ValueError("Currency mismatch")

    balance = get_account_balance(db, source_account_id)
    if balance < amount:
        raise ValueError("Insufficient funds")

    tx = Transaction(
        type=TransactionType.transfer,
        source_account_id=source_account_id,
        destination_account_id=destination_account_id,
        amount=amount,
        currency=currency,
        status=TransactionStatus.pending,
        description=description,
    )
    db.add(tx)
    db.flush()

    debit = LedgerEntry(
        account_id=source_account_id,
        transaction_id=tx.id,
        entry_type=LedgerEntryType.debit,
        amount=amount,
    )

    credit = LedgerEntry(
        account_id=destination_account_id,
        transaction_id=tx.id,
        entry_type=LedgerEntryType.credit,
        amount=amount,
    )

    db.add_all([debit, credit])

    tx.status = TransactionStatus.completed
    return tx
