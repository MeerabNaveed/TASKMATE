from database.db import get_connection
from database.users import get_user_id

def add_task(username, task):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (user_id, task) VALUES (?, ?)", (uid, task))
    conn.commit()
    conn.close()

def get_tasks(username):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, task, status, timestamp FROM tasks WHERE user_id=?", (uid,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_task_stats(username):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT COUNT(*),
                 SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END),
                 SUM(CASE WHEN status='Pending' THEN 1 ELSE 0 END)
                 FROM tasks WHERE user_id=?""", (uid,))
    total, completed, pending = c.fetchone()
    conn.close()
    return total or 0, completed or 0, pending or 0

def update_task_status(task_id, status):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    