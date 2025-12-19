import enum
from sqlalchemy import (
    Column,
    String,
    Enum,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


# --------------------------
# ENUMS
# --------------------------

class AccountType(enum.Enum):
    checking = "checking"
    savings = "savings"


class AccountStatus(enum.Enum):
    active = "active"
    frozen = "frozen"
    closed = "closed"


# --------------------------
# ACCOUNT MODEL
# --------------------------

class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)

    account_type = Column(Enum(AccountType), nullable=False)
    currency = Column(String(3), nullable=False)

    status = Column(Enum(AccountStatus), nullable=False, default=AccountStatus.active)

    # Relationships
    ledger_entries = relationship(
        "LedgerEntry",
        back_populates="account",
        lazy="selectin"
    )
