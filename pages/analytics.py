import streamlit as st
from database.tasks import get_task_stats
from database.chats import load_chat_list, load_chat

def analytics_page():
    st.markdown("## 📊 Analytics Dashboard")
    user = st.session_state["user"]
    
    # Task Stats
    total, completed, pending = get_task_stats(user)
    
    st.subheader("📝 Task Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Tasks", total)
    c2.metric("✅ Completed", completed)
    c3.metric("⏳ Pending", pending)
    
    if total > 0:
        progress_value = completed / total
        st.progress(progress_value)
        st.write(f"**{int(progress_value * 100)}% Complete**")
        
    st.divider()
    
    # Chat Stats
    st.subheader("💬 Chat Engagement")
    chats = load_chat_list(user)
    total_chats = len(chats)
    
    if total_chats > 0:
        total_msgs = 0
        user_msgs = 0
        ai_msgs = 0
        
        # Calculate chat stats
        for chat_id, _, _ in chats:
            msgs = load_chat(user, chat_id)
            total_msgs += len(msgs)
            for role, _, _ in msgs:
                if role == "user":
                    user_msgs += 1
                else:
                    ai_msgs += 1
                    
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Chats", total_chats)
        c2.metric("🧑 Your Messages", user_msgs)
        c3.metric("🤖 AI Messages", ai_msgs)
        
        st.bar_chart({"User": [user_msgs], "AI": [ai_msgs]})
    else:
        st.info("No chat data available yet.")