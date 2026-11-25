import bcrypt
from database.db import get_connection

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password, hashed):
    try:
        if isinstance(hashed, str):
            hashed = hashed.encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), hashed)
    except Exception:
        return False

def create_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    try:
        hashed = hash_password(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True, "Account created!"
    except Exception:
        return False, "Username already exists."
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and verify_password(password, row[2]):
        return {"id": row[0], "username": row[1]}
    return None

def get_user_id(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None