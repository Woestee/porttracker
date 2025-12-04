import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "portfolio.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # access by column name
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            shares INTEGER NOT NULL,
            price REAL NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def add_holding(ticker: str, shares: int, price: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO holdings (ticker, shares, price) VALUES (?, ?, ?)",
        (ticker, shares, price)
    )
    conn.commit()
    conn.close()


def get_portfolio():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, ticker, shares, price FROM holdings")
    rows = cur.fetchall()
    conn.close()

    portfolio = []
    for row in rows:
        value = row["shares"] * row["price"]
        portfolio.append({
            "id": row["id"],
            "ticker": row["ticker"],
            "shares": row["shares"],
            "price": row["price"],
            "value": value
        })
    return portfolio


def delete_holding(holding_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM holdings WHERE id = ?", (holding_id,))
    conn.commit()
    conn.close()
