import time
import sqlite3
import winsound
from datetime import datetime, timedelta
from plyer import notification

def check_events():
    conn = sqlite3.connect("taskmate.db")
    c = conn.cursor()
    try:
        c.execute("SELECT title, date, time, notify_before FROM events")
        events = c.fetchall()
        now = datetime.now()
        
        for title, date, time, notify_before in events:
            try:
                event_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
                # Notification time calculate karein (Event time - notify_before minutes)
                notify_time = event_dt - timedelta(minutes=int(notify_before))
                
                # Agar abhi ka time notification time ke 30 seconds ke andar hai
                if abs((now - notify_time).total_seconds()) <= 30:
                    notification.notify(
                        title="⏰ TaskMate Reminder!",
                        message=f"{title} is due in {notify_before} minutes!",
                        timeout=10,
                    )
                    winsound.Beep(1000, 500)
                    time.sleep(60)  # 1 minute wait karein taake dobara na aaye
            except:
                pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

while True:
    check_events()
    time.sleep(10)  # Har 10 second baad check karein (taake exact time par notification aaye)