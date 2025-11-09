from sqlite3 import connect, Row
from config import DB_NAME

def get_db():
    conn = connect(DB_NAME)
    conn.row_factory = Row

    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # initialize tables
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(100) NOT NULL UNIQUE,
            bio TEXT DEFAULT NULL,
            birth_year INTEGER
        );
    """)
    
    conn.commit()
    conn.close()
