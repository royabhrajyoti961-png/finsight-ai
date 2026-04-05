import sqlite3

def connect():
    return sqlite3.connect("database.db", check_same_thread=False)

def create_table():
    conn = connect()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            note TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()

def add_transaction(amount, category, note, date):
    conn = connect()
    c = conn.cursor()

    c.execute(
        "INSERT INTO transactions (amount, category, note, date) VALUES (?, ?, ?, ?)",
        (amount, category, note, date)
    )

    conn.commit()
    conn.close()

def get_transactions():
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT * FROM transactions")
    data = c.fetchall()

    conn.close()
    return data

def delete_transaction(id):
    conn = connect()
    c = conn.cursor()

    c.execute("DELETE FROM transactions WHERE id=?", (id,))
    conn.commit()
    conn.close()
