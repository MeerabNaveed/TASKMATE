import streamlit as st
from datetime import datetime
from utils.styles import LOGO_BASE64
from database.tasks import get_task_stats

def home_page():
    # Logo Bada kiya gaya hai (width: 280px)
    if LOGO_BASE64:
        st.markdown(f'<div style="text-align:center; margin-bottom: 1.5rem;"><img src="data:image/png;base64,{LOGO_BASE64}" style="width:280px; border-radius:15px;"/></div>', unsafe_allow_html=True)

    hour = datetime.now().hour
    greeting = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    st.markdown(f"## {greeting}, {st.session_state['user']} 👋")

    # Metrics
    total, completed, pending = get_task_stats(st.session_state["user"])
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card"><div class="metric-value">{total}</div><div>📝 Total Tasks</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#22C55E;">{completed}</div><div>✅ Completed</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#F59E0B;">{pending}</div><div>⏳ Pending</div></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📌 All Modules")
    
    modules = [
        "💬 New Chat", "📜 Chat History", "📝 Tasks", 
        "📅 Calendar", "📊 Analytics", "🎓 Study Tools", 
        "📂 Documents", "📧 Email Drafting", "🖼️ Image Generation", 
        "🎙️ Voice Assistant", "📊 PPT Generator"
    ]
    
    # 3 columns banaye hain taake buttons elongated na hon
    cols = st.columns(3)
    for i, m in enumerate(modules):
        with cols[i % 3]:
            if st.button(m, key=f"mod_{i}", use_container_width=True):
                st.session_state["page"] = m
                st.rerun()