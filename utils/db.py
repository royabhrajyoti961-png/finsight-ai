import sqlite3

def connect():
    return sqlite3.connect("database.db", check_same_thread=False)

def create_tables():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
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

def register_user(username, password):
    conn = connect()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except Exception as e:
        print("REGISTER ERROR:", e)
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def add_expense(user_id, amount, category, note, date):
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO transactions (user_id, amount, category, note, date) VALUES (?, ?, ?, ?, ?)",
              (user_id, amount, category, note, date))
    conn.commit()
    conn.close()

def get_expenses(user_id):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM transactions WHERE user_id=?", (user_id,))
    data = c.fetchall()
    conn.close()
    return data

def delete_expense(expense_id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()
