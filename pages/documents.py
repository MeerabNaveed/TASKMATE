import streamlit as st
from utils.ai import get_ai_reply
from utils.file_reader import read_uploaded_file

def documents_page():
    st.markdown("## 📂 Document Processing")
    
    uploaded = st.file_uploader("Upload Document", type=["txt", "pdf", "docx", "csv", "xlsx"])
    
    if uploaded:
        with st.spinner("Reading file..."):
            content = read_uploaded_file(uploaded)
            
        if content:
            st.info(f"📄 File loaded: {uploaded.name}")
            with st.expander("Preview Content"):
                st.text(content[:1000] + "\n..." if len(content) > 1000 else content)
                
            st.divider()
            
            # Input aur Button ko ek line mein lane ke liye
            col1, col2 = st.columns([4, 1])
            
            with col1:
                action = st.text_input("What should I do with this document?", placeholder="e.g., Summarize, Extract key points...", label_visibility="collapsed")
            with col2:
                st.write("") # Alignment spacing
                process_btn = st.button("Process Document", type="primary", use_container_width=True)
                
            if process_btn:
                if action:
                    with st.spinner("Processing..."):
                        reply = get_ai_reply(f"Action: {action}\n\nDocument Content:\n{content[:4000]}")
                    st.success("✅ Processed!")
                    st.markdown(reply)
                    
                    st.download_button(
                        label="📥 Download Result",
                        data=reply,
                        file_name="document_result.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                else:
                    st.warning("Please enter an action (e.g., Summarize).")
        else:
            st.error("Could not read the file content. It might be empty or corrupted.")