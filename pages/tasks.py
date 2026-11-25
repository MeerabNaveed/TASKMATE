import streamlit as st
from database.tasks import add_task, get_tasks, update_task_status, delete_task

def tasks_page():
    st.markdown("## 📝 Task Manager")
    user = st.session_state["user"]
    
    c1, c2 = st.columns([4, 1])
    with c1:
        new_task = st.text_input("Add a new task", placeholder="Enter task...", label_visibility="collapsed")
    with c2:
        if st.button("Add", type="primary", use_container_width=True) and new_task.strip():
            add_task(user, new_task)
            st.rerun()

    st.divider()
    
    tasks = get_tasks(user)
    if not tasks:
        st.info("No tasks yet. Add one above!")
        return
        
    for tid, task, status, ts in tasks:
        c1, c2, c3 = st.columns([4, 1, 1])
        with c1:
            checked = st.checkbox(task, value=(status == "Completed"), key=f"t_{tid}")
            if checked != (status == "Completed"):
                update_task_status(tid, "Completed" if checked else "Pending")
                st.rerun()
            st.caption(f"🕐 {ts}")
        with c2:
            st.markdown("✅ Done" if status == "Completed" else "⏳ Pending")
        with c3:
            if st.button("🗑️", key=f"d_{tid}"):
                delete_task(tid)
                st.rerun()