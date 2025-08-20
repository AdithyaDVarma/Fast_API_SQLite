import sqlite3

DB_FILE = "bank.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Accounts table with type & status
    c.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL DEFAULT 'savings', -- savings or current
            balance REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'active' -- active or inactive
        )
    """)

    # Transactions table
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            account_id INTEGER,
            target_account_id INTEGER,
            amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def create_account(name: str, acc_type: str = "savings") -> int:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO accounts (name, type, balance, status) VALUES (?, ?, ?, ?)", 
              (name, acc_type, 0.0, "active"))
    conn.commit()
    account_id = c.lastrowid
    conn.close()
    return account_id

def get_account(account_id: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, type, balance, status FROM accounts WHERE id=?", (account_id,))
    row = c.fetchone()
    conn.close()
    return row

def get_all_accounts():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, type, balance, status FROM accounts")
    rows = c.fetchall()
    conn.close()
    return rows

def search_accounts_by_name(name: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, type, balance, status FROM accounts WHERE name LIKE ?", (f"%{name}%",))
    rows = c.fetchall()
    conn.close()
    return rows

def update_balance(account_id: int, amount: float):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE accounts SET balance = balance + ? WHERE id=?", (amount, account_id))
    conn.commit()
    conn.close()

    log_transaction("deposit" if amount > 0 else "withdraw", account_id, None, abs(amount))

def transfer_money(from_id: int, to_id: int, amount: float):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT balance FROM accounts WHERE id=?", (from_id,))
    row = c.fetchone()
    if not row or row[0] < amount:
        conn.close()
        raise ValueError("Insufficient balance")

    c.execute("UPDATE accounts SET balance = balance - ? WHERE id=?", (amount, from_id))
    c.execute("UPDATE accounts SET balance = balance + ? WHERE id=?", (amount, to_id))
    conn.commit()
    conn.close()

    log_transaction("transfer", from_id, to_id, amount)

def deactivate_account(account_id: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE accounts SET status='inactive' WHERE id=?", (account_id,))
    conn.commit()
    conn.close()

def get_total_balance():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT SUM(balance) FROM accounts WHERE status='active'")
    total = c.fetchone()[0] or 0
    conn.close()
    return total

def log_transaction(txn_type: str, account_id: int, target_account_id: int, amount: float):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO transactions (type, account_id, target_account_id, amount)
        VALUES (?, ?, ?, ?)
    """, (txn_type, account_id, target_account_id, amount))
    conn.commit()
    conn.close()

def get_transactions(account_id: int, txn_type: str = None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if txn_type:
        c.execute("""
            SELECT id, type, account_id, target_account_id, amount, timestamp
            FROM transactions
            WHERE (account_id=? OR target_account_id=?) AND type=?
            ORDER BY timestamp DESC
        """, (account_id, account_id, txn_type))
    else:
        c.execute("""
            SELECT id, type, account_id, target_account_id, amount, timestamp
            FROM transactions
            WHERE account_id=? OR target_account_id=?
            ORDER BY timestamp DESC
        """, (account_id, account_id))
    rows = c.fetchall()
    conn.close()
    return rows

def apply_interest(rate: float = 0.02):
    """Apply interest to all savings accounts"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE accounts SET balance = balance + (balance * ?) WHERE type='savings' AND status='active'", (rate,))
    conn.commit()
    conn.close()

def get_top_accounts(limit: int = 5):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, type, balance FROM accounts WHERE status='active' ORDER BY balance DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
