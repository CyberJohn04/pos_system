import sqlite3

def get_connection():
    return sqlite3.connect("pos.db")

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create product table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()