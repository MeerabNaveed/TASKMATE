from database.db import get_connection
from database.users import get_user_id

def get_next_chat_id(username):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT MAX(chat_id) FROM chats WHERE user_id=?", (uid,))
    max_id = c.fetchone()[0]
    conn.close()
    return (max_id or 0) + 1

def save_chat(username, role, message, chat_id=1):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO chats (user_id, role, message, chat_id) VALUES (?, ?, ?, ?)",
              (uid, role, message, chat_id))
    conn.commit()
    conn.close()

def load_chat(username, chat_id):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT role, message, timestamp FROM chats WHERE user_id=? AND chat_id=? ORDER BY id",
              (uid, chat_id))
    rows = c.fetchall()
    conn.close()
    return rows

def load_chat_list(username):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT chat_id, MIN(timestamp), MAX(pinned)
                 FROM chats WHERE user_id=? GROUP BY chat_id
                 ORDER BY MAX(pinned) DESC, MIN(timestamp) DESC""", (uid,))
    rows = c.fetchall()
    conn.close()
    return rows

def toggle_pin_chat(username, chat_id):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT pinned FROM chats WHERE user_id=? AND chat_id=? LIMIT 1", (uid, chat_id))
    row = c.fetchone()
    if row:
        new = 0 if row[0] == 1 else 1
        c.execute("UPDATE chats SET pinned=? WHERE user_id=? AND chat_id=?", (new, uid, chat_id))
        conn.commit()
    conn.close()

def clear_chat(username, chat_id):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM chats WHERE user_id=? AND chat_id=?", (uid, chat_id))
    conn.commit()
    conn.close()

def build_context(username, chat_id, limit=10):
    history = load_chat(username, chat_id)
    context = ""
    for role, msg, _ in history[-limit:]:
        context += f"{role}: {msg}\n"
    return context
