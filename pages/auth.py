import time
import streamlit as st
from utils.styles import LOGO_BASE64
from database.users import create_user, authenticate_user

def login_page():
    # Logo ko bada kiya (width: 300px)
    if LOGO_BASE64:
        st.markdown(f'<div style="text-align:center; margin-top: 2rem; margin-bottom: 1rem;"><img src="data:image/png;base64,{LOGO_BASE64}" style="width:300px; border-radius:16px;"/></div>', unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align:center; margin-top: 2rem;'>✨ TaskMate</h1>", unsafe_allow_html=True)

    # Form ko center mein lane ke liye columns
    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        st.subheader("🔑 Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login", type="primary", use_container_width=True):
                user = authenticate_user(username, password)
                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = user["username"]
                    st.session_state["page"] = "🏠 Home"
                    st.session_state["last_activity"] = time.time()
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        st.divider()
        st.markdown("<p style='text-align:center;'>New here?</p>", unsafe_allow_html=True)
        if st.button("Create Account", use_container_width=True):
            st.session_state["page"] = "🆕 Signup"
            st.rerun()

def signup_page():
    if LOGO_BASE64:
        st.markdown(f'<div style="text-align:center; margin-top: 2rem; margin-bottom: 1rem;"><img src="data:image/png;base64,{LOGO_BASE64}" style="width:250px; border-radius:16px;"/></div>', unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        st.subheader("🆕 Sign Up")
        with st.form("signup_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            if st.form_submit_button("Sign Up", type="primary", use_container_width=True):
                if not username or not password:
                    st.error("Please fill all fields")
                elif password != confirm:
                    st.error("Passwords don't match")
                else:
                    ok, msg = create_user(username, password)
                    if ok:
                        st.success(msg + " Please login.")
                        st.session_state["page"] = "🔑 Login"
                        st.rerun()
                    else:
                        st.error(msg)

        st.divider()
        if st.button("Back to Login", use_container_width=True):
            st.session_state["page"] = "🔑 Login"
            st.rerun()