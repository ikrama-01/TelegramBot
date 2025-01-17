import sqlite3
from datetime import datetime

def get_connection(db_path="bot.db"):
    """Establish and return a database connection."""
    conn = sqlite3.connect(db_path, check_same_thread=False)
    sqlite3.register_adapter(datetime, lambda d: d.strftime('%Y-%m-%d %H:%M:%S'))
    sqlite3.register_converter("datetime", lambda s: datetime.strptime(s.decode(), '%Y-%m-%d %H:%M:%S'))
    
    return conn

def initialize_database():
    """Initialize the database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            role TEXT,
            role_selected INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            task TEXT,
            status TEXT DEFAULT 'pending',
            deadline TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subsidiaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            manager TEXT,
            revenue REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
