from fastapi import FastAPI

from app.database import Base, engine
from app.routers import accounts, transactions

# Import models so SQLAlchemy registers them
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.ledger import LedgerEntry

app = FastAPI(title="Financial Ledger API")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(accounts.router)
app.include_router(transactions.router)


@app.get("/health")
def health():
    return {"status": "ok"}
