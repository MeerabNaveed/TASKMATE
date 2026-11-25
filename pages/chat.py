import streamlit as st
from datetime import datetime
from database.chats import (get_next_chat_id, save_chat, load_chat,
                            load_chat_list, toggle_pin_chat, clear_chat, build_context)
from utils.ai import get_ai_reply

def new_chat_page():
    user = st.session_state["user"]
    
    if "active_chat_id" not in st.session_state:
        st.session_state["active_chat_id"] = get_next_chat_id(user)

    chat_id = st.session_state["active_chat_id"]
    
    # ==========================================
    # HEADER (Chat Title & New Chat Button)
    # ==========================================
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("## 💬 Chat")
        st.caption(f"Chat #{chat_id} • {datetime.now().strftime('%B %d, %Y')}")
    with col2:
        st.write("") # Spacing
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state["active_chat_id"] = get_next_chat_id(user)
            st.session_state["msg_count"] = 0
            st.rerun()

    st.divider()

    # ==========================================
    # CHAT HISTORY DISPLAY
    # ==========================================
    messages = load_chat(user, chat_id)
    for role, msg, ts in messages:
        if role == "user":
            st.markdown(f'<div style="text-align:right"><div class="user-bubble" style="display:inline-block">{msg}</div><div style="font-size:0.7rem;color:gray">You • {ts}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:left"><div class="assistant-bubble" style="display:inline-block">{msg}</div><div style="font-size:0.7rem;color:gray">TaskMate • {ts}</div></div>', unsafe_allow_html=True)

    st.divider()

    # ==========================================
    # INPUT & SEND BUTTON (Ek hi line mein)
    # ==========================================
    if "msg_count" not in st.session_state:
        st.session_state["msg_count"] = 0

    # 6:1 ratio means Text box bada hoga, button chota
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_area("Message", height=80, placeholder="Type your message here...", label_visibility="collapsed")
        
    with col2:
        st.write("") # Button ko thoda neeche align karne ke liye
        st.write("") 
        if st.button("📤 Send", type="primary", use_container_width=True):
            if st.session_state["msg_count"] >= 20:
                st.warning("⚠️ Rate limit: 20 messages per session.")
            elif user_input.strip():
                # User message save karein
                save_chat(user, "user", user_input, chat_id)
                
                # AI context banayein
                context = build_context(user, chat_id, limit=10)
                
                with st.spinner("🤔 Thinking..."):
                    reply = get_ai_reply(user_input, context)
                    
                # AI message save karein
                save_chat(user, "assistant", reply, chat_id)
                
                st.session_state["msg_count"] += 1
                st.rerun()


def chat_list_page():
    st.markdown("## 📜 Chat History")
    user = st.session_state["user"]
    search = st.text_input("🔍 Search chats...")
    
    chats = load_chat_list(user)
    if not chats:
        st.info("No chats yet. Start a new conversation!")
        return
        
    for chat_id, ts, pinned in chats:
        msgs = load_chat(user, chat_id)
        
        # Search filter
        if search and not any(search.lower() in m[1].lower() for m in msgs):
            continue
            
        preview = msgs[0][1][:80] + "..." if msgs else "Empty"
        
        c1, c2, c3 = st.columns([4, 1, 1])
        with c1:
            icon = "📌" if pinned else "💬"
            st.markdown(f'<div class="card"><b>{icon} Chat #{chat_id}</b><br><small>{preview}</small></div>', unsafe_allow_html=True)
        with c2:
            if st.button("View", key=f"v_{chat_id}", use_container_width=True):
                st.session_state["selected_chat"] = chat_id
                st.session_state["page"] = "📜 View Chat"
                st.rerun()
        with c3:
            if st.button("📍" if pinned else "📌", key=f"p_{chat_id}", use_container_width=True):
                toggle_pin_chat(user, chat_id)
                st.rerun()


def view_specific_chat():
    if "selected_chat" not in st.session_state:
        st.warning("No chat selected.")
        return
        
    user = st.session_state["user"]
    chat_id = st.session_state["selected_chat"]
    
    if st.button("⬅️ Back to Chats"):
        st.session_state["page"] = "📜 Chat History"
        st.rerun()
        
    st.markdown(f"## 💬 Chat #{chat_id}")
    
    for role, msg, ts in load_chat(user, chat_id):
        if role == "user":
            st.markdown(f'<div style="text-align:right"><div class="user-bubble" style="display:inline-block">{msg}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:left"><div class="assistant-bubble" style="display:inline-block">{msg}</div></div>', unsafe_allow_html=True)
            
    st.divider()
    if st.button("🗑️ Delete Chat", type="primary", use_container_width=True):
        clear_chat(user, chat_id)
        st.session_state.pop("selected_chat", None)
        st.session_state["page"] = "📜 Chat History"
        st.rerun()
