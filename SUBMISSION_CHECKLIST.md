# 📝 **Submission Summary**

This project implements a fully ACID-compliant financial ledger system using **double-entry bookkeeping**, **immutable ledger entries**, **row-level locking**, and **transaction-safe accounting logic**.

Evaluators can validate the reliability and correctness of the system through controlled financial operations such as deposits, withdrawals, and transfers — all of which produce balanced ledger entries and accurate account balances derived entirely from transaction history.

---

# 🔍 **What Evaluators Should Test**

### ✅ 1. Application Startup

* Run PostgreSQL via Docker:

  ```sh
  docker compose up -d
  ```
* Run API server:

  ```sh
  uvicorn app.main:app --reload
  ```

### ✅ 2. API Health

* Test endpoint: `/health`
* Expect: `{ "status": "ok" }`

### ✅ 3. Account Operations

* Create two accounts
* Validate account properties (id, currency, status)

### ✅ 4. Deposit / Withdrawal

* Deposit into account_1
* Withdraw from account_2
* Confirm balances are updated correctly

### ✅ 5. Transfer Operation

* Transfer between internal accounts
* Validate:

  * One **debit ledger entry**
  * One **credit ledger entry**
  * Equal amounts
  * Same `transaction_id`
  * Transaction status = `completed`

### ✅ 6. Negative Balance Protection

Attempt:

* Withdraw more than available balance
* Transfer more than available balance

Expect:

```
422 Unprocessable Entity
```

or custom error message:

```
"Insufficient funds"
```

### ✅ 7. Ledger Immutability

* Ledger entries must **never** update or delete
* New operations append **new entries only**

### ✅ 8. Balance Calculation Integrity

* Balance returned by `/accounts/{id}` must equal:

```
SUM(credits) - SUM(debits)
```

### ✅ 9. Concurrency Safety (Optional but Validates System Strength)

Perform **two simultaneous transfers** from account_1.
Expected outcome:

* Only one should succeed
* The other should fail due to insufficient funds **after row-level locking**
* Ledger should remain consistent

---

# 📁 **Files Included in Submission**

| File                                           | Purpose              |
| ---------------------------------------------- | -------------------- |
| `app/`                                         | Full API source code |
| `docker-compose.yml`                           | PostgreSQL database  |
| `requirements.txt`                             | Python dependencies  |
| `Financial-Ledger-API.postman_collection.json` | End-to-end API tests |
| `README.md`                                    | Full documentation   |
| Architecture diagram                           | System flow          |
| ERD diagram                                    | Database structure   |

---

# 📦 **Submission Checklist**

Add this EXACT checklist to your README so evaluators can verify your work:

```markdown
# ✔ Submission Checklist

- [x] Project repository contains full working code
- [x] Docker Compose file starts PostgreSQL successfully
- [x] FastAPI application starts without errors
- [x] README includes:
  - [x] Setup instructions
  - [x] Design decisions
  - [x] Architecture diagram (Mermaid)
  - [x] ERD diagram (Mermaid)
  - [x] SQL DDL schema
  - [x] Postman testing workflow
- [x] Ledger entries are immutable (append-only)
- [x] All monetary operations use ACID DB transactions
- [x] Double-entry bookkeeping implemented (balanced ledger)
- [x] Balance computed from ledger only (no stored balance)
- [x] Negative balance protection enforced
- [x] Concurrency safety validated
- [x] Postman collection included for grading
```

---
