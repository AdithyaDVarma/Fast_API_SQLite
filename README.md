# 🏦 Advanced Banking App v2

A simple **banking system API** built with **FastAPI** and **SQLite**.
This project simulates a digital bank where you can create accounts, deposit/withdraw money, transfer funds, and track transactions.

---

## 🚀 Features

* **Create accounts** with `savings` or `current` type.
* **Deposit & Withdraw** money safely.
* **Transfer funds** between accounts.
* **View balance** of any account.
* **Search accounts** by name.
* **Account status**: deactivate accounts instead of deleting them permanently.
* **Bank total**: see total money across all active accounts.
* **Transactions history** with optional filtering (deposit, withdraw, transfer).
* **Apply interest** to all savings accounts.
* **Top accounts**: list richest customers.

---

## 📂 Project Structure

```
.
├── db.py        # Database functions (SQLite: accounts & transactions)
├── main.py      # FastAPI endpoints (REST API)
├── bank.db      # SQLite database file (auto-created)
└── README.md    # Documentation
```

---

## 🛠 Setup Instructions

### 1️⃣ Install Dependencies

```bash
pip install fastapi uvicorn pydantic
```

### 2️⃣ Run the API Server

```bash
uvicorn main:app --reload
```

### 3️⃣ Open API Docs

Visit:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📌 API Endpoints

### 🏗 Account Management

* **Create account** → `POST /create_account/`

  ```json
  { "name": "Alice", "type": "savings" }
  ```
* **List all accounts** → `GET /accounts/`
* **Search accounts** → `GET /accounts/search/{name}`
* **Deactivate account** → `PUT /deactivate_account/{account_id}`

---

### 💰 Money Operations

* **Check balance** → `GET /balance/{account_id}`
* **Deposit** → `POST /deposit/`

  ```json
  { "account_id": 1, "amount": 500 }
  ```
* **Withdraw** → `POST /withdraw/`
* **Transfer** → `POST /transfer/`

  ```json
  { "from_id": 1, "to_id": 2, "amount": 200 }
  ```

---

### 📊 Bank-Wide Features

* **Total bank balance** → `GET /bank_total/`
* **Transaction history** → `GET /transactions/{account_id}`

  * Optional filter: `?txn_type=deposit`
* **Apply interest (default 2%)** → `POST /apply_interest/`
* **Top accounts** → `GET /top_accounts/?limit=5`

---

## 📖 Notes

* Accounts are **deactivated** instead of being deleted to preserve history.
* Transactions are logged automatically for deposits, withdrawals, and transfers.
* By default, **interest = 2%** is applied only to active savings accounts.

---

## 🏗 Tech Stack

* **Backend**: FastAPI
* **Database**: SQLite3

---

## 📜 License

Adobe License – feel free to use & modify.

---
