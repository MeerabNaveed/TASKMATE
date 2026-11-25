import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import time
from dotenv import load_dotenv
from streamlit_js_eval import streamlit_js_eval
from database.notifications import get_notifications, mark_notification_read, check_deadlines
from datetime import datetime

# Load environment variables
load_dotenv()

# ============================================
# 📦 PAGE CONFIG (Must be first Streamlit command)
# ============================================
st.set_page_config(
    page_title="TaskMate",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 📥 IMPORT DATABASE & UTILS
# ============================================
from database.db import init_db
from utils.styles import inject_css, LOGO_BASE64

# ============================================
# 📥 IMPORT PAGES
# ============================================
from pages.auth import login_page, signup_page
from pages.home import home_page
from pages.chat import new_chat_page, chat_list_page, view_specific_chat
from pages.tasks import tasks_page
from pages.calendar import calendar_page
from pages.analytics import analytics_page
from pages.study import study_page
from pages.documents import documents_page
from pages.email import email_page
from pages.image_generator import image_page
from pages.voice import voice_page
from pages.ppt import ppt_page

# ============================================
# 🎨 INJECT CUSTOM CSS
# ============================================
inject_css()

# ============================================
# 🚀 MAIN APP LOGIC
# ============================================
def main():
    # 1. Initialize Database
    init_db()

    # 2. Session Variables Setup
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['page'] = "🔑 Login"
        st.session_state['last_activity'] = time.time()

    # 3. Session Timeout Logic (30 Minutes)
    if st.session_state['logged_in']:
        if time.time() - st.session_state.get('last_activity', time.time()) > 1800:
            st.session_state.clear()
            st.session_state['logged_in'] = False
            st.session_state['page'] = "🔑 Login"
            st.warning("⏳ Session expired. Please login again.")
            st.rerun()
        else:
            st.session_state['last_activity'] = time.time()

    # 4. Routing (Login vs App)
    if not st.session_state['logged_in']:
        if st.session_state['page'] == "🆕 Signup":
            signup_page()
        else:
            login_page()
    else:
        # ==========================================
        # 🔔 REAL-TIME NOTIFICATION ENGINE
        # ==========================================
        user = st.session_state['user']
        
        # Deadline check karein
        check_deadlines(user)
        
        # Un-read notifications fetch karein
        notifs = get_notifications(user)
        unread = [n for n in notifs if n[4] == 0]
        
        if unread:
            notif = unread[0]
            notif_id = notif[0]
            title = notif[1]
            msg = notif[2]
            
            # Browser Notification Code
            js_code = f"""
                if (Notification.permission === "granted") {{
                    new Notification("{title}", {{ body: "{msg}" }});
                }} else if (Notification.permission !== "denied") {{
                    Notification.requestPermission().then(permission => {{
                        if (permission === "granted") {{
                            new Notification("{title}", {{ body: "{msg}" }});
                        }}
                    }});
                }}
            """
            streamlit_js_eval(js_expressions=js_code, key=f"notif_{notif_id}")
            
            # Mark as read
            mark_notification_read(notif_id)
            
            # App ke andar toast message
            st.toast(f"🔔 {title}: {msg}", icon="⚠️")

        # ==========================================
        # 🔐 SIDEBAR NAVIGATION
        # ==========================================
        with st.sidebar:
            if LOGO_BASE64:
                st.markdown(f'<div class="sidebar-logo-container"><img src="data:image/png;base64,{LOGO_BASE64}" class="sidebar-logo" alt="TaskMate"/></div>', unsafe_allow_html=True)
            else:
                st.markdown('<h2 style="text-align: center;">✨ TaskMate</h2>', unsafe_allow_html=True)
            
            st.divider()
            
            pages = [
                "🏠 Home",
                "💬 New Chat",
                "📜 Chat History",
                "📝 Tasks",
                "📅 Calendar",
                "📊 Analytics",
                "🎓 Study Tools", 
                "📂 Documents",
                "📧 Email Drafting",
                "🖼️ Image Generation",
                "🎙️ Voice Assistant",
                "📊 PPT Generator"
            ]
            
            for page in pages:
                if st.button(page, use_container_width=True):
                    st.session_state['page'] = page
                    st.rerun()
            
            st.divider()
            
            st.markdown('<div class="logout-container">', unsafe_allow_html=True)
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.clear()
                st.session_state['logged_in'] = False
                st.session_state['page'] = "🔑 Login"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================
        # 📄 PAGE ROUTING
        # ==========================================
        current_page = st.session_state.get('page', "🏠 Home")

        if current_page == "🏠 Home":
            home_page()
        elif current_page == "💬 New Chat":
            new_chat_page()
        elif current_page == "📜 Chat History":
            chat_list_page()
        elif current_page == "📜 View Chat":
            view_specific_chat()
        elif current_page == "📝 Tasks":
            tasks_page()
        elif current_page == "📅 Calendar":
            calendar_page()
        elif current_page == "📊 Analytics":
            analytics_page()
        elif current_page == "🎓 Study Tools":
            study_page()
        elif current_page == "📂 Documents":
            documents_page()
        elif current_page == "📧 Email Drafting":
            email_page()
        elif current_page == "🖼️ Image Generation":
            image_page()
        elif current_page == "🎙️ Voice Assistant":
            voice_page()
        elif current_page == "📊 PPT Generator":
            ppt_page()
        else:
            home_page()

# ============================================
# 🏃 RUN APP
# ============================================
if __name__ == "__main__":
    main()