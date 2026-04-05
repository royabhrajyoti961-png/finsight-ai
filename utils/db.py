import sqlite3

def connect():
    return sqlite3.connect("database.db", check_same_thread=False)

def create_tables():
    conn = connect()
    c = conn.cursor()

    # 🔥 Force fresh schema (IMPORTANT)
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS transactions")

    c.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        category TEXT,
        note TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

def register(username, password):
    conn = connect()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login(username, password):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()
    conn.close()
    return data

def add_transaction(user_id, amount, category, note, date):
    conn = connect()
    c = conn.cursor()
    c.execute(
        "INSERT INTO transactions (user_id, amount, category, note, date) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, category, note, date)
    )
    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM transactions WHERE user_id=?", (user_id,))
    data = c.fetchall()
    conn.close()
    return data

def delete_transaction(id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id=?", (id,))
    conn.commit()
    conn.close()
