import enum
import uuid
from sqlalchemy import Column, String, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from app.database import Base


# --------------------------
# ENUMS
# --------------------------

class TransactionType(enum.Enum):
    transfer = "transfer"
    deposit = "deposit"
    withdrawal = "withdrawal"


class TransactionStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


# --------------------------
# TRANSACTION MODEL
# --------------------------

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    type = Column(Enum(TransactionType), nullable=False)

    source_account_id = Column(UUID(as_uuid=True), nullable=True)
    destination_account_id = Column(UUID(as_uuid=True), nullable=True)

    amount = Column(Numeric(18, 4), nullable=False)
    currency = Column(String(3), nullable=False)

    status = Column(Enum(TransactionStatus), nullable=False, default=TransactionStatus.pending)

    description = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    ledger_entries = relationship(
        "LedgerEntry",
        back_populates="transaction",
        lazy="selectin"
    )
