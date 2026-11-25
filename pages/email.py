import streamlit as st
from utils.ai import get_ai_reply

def email_page():
    st.markdown("## 📧 Email Drafting")
    
    st.markdown("""
    <div style="background: rgba(108,99,255,0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        Let AI draft professional emails for you in seconds.
    </div>
    """, unsafe_allow_html=True)
    
    # Form hata diya hai taake error na aaye
    to = st.text_input("To (Recipient)", placeholder="e.g., HR Manager, Client...")
    subject = st.text_input("Subject", placeholder="e.g., Leave Application, Project Update...")
    context = st.text_area("Context / Details", placeholder="What do you want to say?")
        
    if st.button("✨ Generate Email", type="primary", use_container_width=True):
        if to and subject:
            with st.spinner("Drafting email..."):
                prompt = f"Write a professional email to {to} regarding {subject}. Context: {context}"
                reply = get_ai_reply(prompt)
            
            st.success("✅ Email Drafted!")
            st.text_area("Draft (Copy from here)", reply, height=250)
            
            st.download_button(
                label="📥 Download Draft",
                data=reply,
                file_name="email_draft.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.warning("Please fill in 'To' and 'Subject' fields.")