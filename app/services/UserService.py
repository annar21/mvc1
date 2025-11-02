from app.utils.db import get_db

def create_user(usr, pwd):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (usr,))
    candidate = cursor.fetchone()

    if candidate:
        raise Exception("User with that username already exists")

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (usr, pwd)) 
    db.commit()

    return {
        "id": cursor.lastrowid,
        "username": usr,
        "password": pwd
    }