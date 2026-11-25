from database.db import get_connection
from database.users import get_user_id
from datetime import datetime

def add_notification(username, title, message, deadline=None):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO notifications (user_id, title, message, deadline) VALUES (?, ?, ?, ?)",
        (uid, title, message, deadline),
    )
    conn.commit()
    conn.close()

def get_notifications(username):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT id, title, message, deadline, is_read, created_at FROM notifications WHERE user_id=? ORDER BY created_at DESC",
        (uid,),
    )
    rows = c.fetchall()
    conn.close()
    return rows

def mark_notification_read(notif_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE notifications SET is_read=1 WHERE id=?", (notif_id,))
    conn.commit()
    conn.close()

def check_deadlines(username):
    uid = get_user_id(username)
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT id, task, timestamp FROM tasks WHERE user_id=? AND status='Pending'", (uid,))
        tasks = c.fetchall()
        for task_id, task, timestamp in tasks:
            if timestamp:
                # Date parse karein
                try:
                    deadline = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue
                    
                days_left = (deadline - datetime.now()).days
                
                # Check karein ke pehle se notification toh nahi hai
                c.execute("SELECT id FROM notifications WHERE user_id=? AND message LIKE ?", (uid, f"%{task}%"))
                if not c.fetchone():
                    if days_left == 1:
                        add_notification(username, "⏰ Task Deadline Tomorrow", f"Task: {task}")
                    elif days_left == 0:
                        add_notification(username, "🚨 Task Due Today!", f"Task: {task} is due today!")
                    elif days_left < 0:
                        add_notification(username, "⚠️ Task Overdue", f"Task: {task} is overdue!")
    except Exception as e:
        print(f"Deadline check error: {e}")
    finally:
        conn.close()