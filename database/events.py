from database.db import get_connection
from database.users import get_user_id

def add_event(username, title, date, time, description, notify_before):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO events (user_id, title, date, time, description, notify_before) VALUES (?, ?, ?, ?, ?, ?)",
              (uid, title, date, time, description, notify_before))
    conn.commit()
    conn.close()

def get_events(username):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT title, date, time, description, notify_before FROM events WHERE user_id=? ORDER BY date", (uid,))
    rows = c.fetchall()
    conn.close()
    return rows
