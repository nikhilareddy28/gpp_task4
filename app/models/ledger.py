import enum
import uuid
from sqlalchemy import Column, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from app.database import Base


# --------------------------
# ENUMS
# --------------------------

class LedgerEntryType(enum.Enum):
    debit = "debit"
    credit = "credit"


# --------------------------
# LEDGER ENTRY MODEL
# --------------------------

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        nullable=False
    )

    transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id", ondelete="RESTRICT"),
        nullable=False
    )

    entry_type = Column(Enum(LedgerEntryType), nullable=False)

    amount = Column(Numeric(18, 4), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    account = relationship("Account", back_populates="ledger_entries")
    transaction = relationship("Transaction", back_populates="ledger_entries")
