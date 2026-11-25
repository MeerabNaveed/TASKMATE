import streamlit as st
from database.events import add_event, get_events

def calendar_page():
    st.markdown("## 📅 Calendar")
    user = st.session_state["user"]
    
    with st.container():
        st.subheader("➕ Add New Event")
        with st.form("event_form"):
            title = st.text_input("Event Title", placeholder="Enter event title...")
            c1, c2 = st.columns(2)
            with c1:
                date = st.date_input("Date")
            with c2:
                time = st.time_input("Time")
                
            desc = st.text_area("Description", placeholder="Event description...")
            notify = st.selectbox("⏰ Notify before (minutes)", [5, 10, 15, 30, 60, 120, 1440], index=2)
            
            if st.form_submit_button("Add Event", type="primary", use_container_width=True):
                if title:
                    add_event(user, title, str(date), str(time), desc, notify)
                    st.success("✅ Event added successfully!")
                    st.rerun()
                else:
                    st.warning("Please enter an event title.")

    st.divider()
    
    events = get_events(user)
    if not events:
        st.info("No events scheduled yet.")
        return
        
    st.subheader("📋 Your Events")
    for title, date, time, desc, notify in events:
        # Notification string formatting
        if notify < 60:
            n_str = f"{notify} mins before"
        elif notify < 1440:
            n_str = f"{notify//60} hours before"
        else:
            n_str = f"{notify//1440} days before"
            
        st.markdown(f'''
        <div class="card" style="margin-bottom: 10px;">
            <h4 style="margin: 0; color: #6C63FF;">{title}</h4>
            <p style="margin: 5px 0;">📅 {date} at {time}</p>
            <p style="margin: 5px 0; color: gray;">📝 {desc or "No description"}</p>
            <small style="color: #FF6584;">⏰ Notification: {n_str}</small>
        </div>
        ''', unsafe_allow_html=True)