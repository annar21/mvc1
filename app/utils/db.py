from sqlite3 import connect, Row
from config import DB_NAME

def get_db():
    conn = connect(DB_NAME)
    conn.row_factory = Row

    return conn


def init_db():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL                
    )""")