import streamlit as st
from utils.ai import get_ai_reply
from utils.file_reader import read_uploaded_file

def study_page():
    st.markdown("## 🎓 Study Tools")
    
    tool = st.selectbox("Choose a tool", [
        "🎓 MCQ Generator", 
        "📖 Flashcards", 
        "📊 Comparison Table",
        "📐 Formula Sheets", 
        "🧠 Mnemonics"
    ])
    
    st.divider()
    
    # Tool ke hisaab se inputs dikhayein
    if "Comparison" in tool:
        c1, c2 = st.columns(2)
        with c1: item1 = st.text_input("Item 1", placeholder="e.g., Analog")
        with c2: item2 = st.text_input("Item 2", placeholder="e.g., Digital")
        topic = f"{item1} vs {item2}"
        num_items = None
        uploaded = None
    else:
        uploaded = st.file_uploader("Upload notes (Optional)", type=["txt", "pdf", "docx"])
        topic = st.text_input("Or enter a topic", placeholder="e.g., World War 2...")
        
        num_items = 5
        if "MCQ" in tool or "Flashcard" in tool:
            num_items = st.number_input("How many items to generate?", min_value=1, max_value=50, value=5)

    if st.button("✨ Generate", type="primary", use_container_width=True):
        content = read_uploaded_file(uploaded) if uploaded else None
        source = content if content else topic
        
        if not source:
            st.warning("Please upload a file OR enter a topic.")
            return
            
        prompt = ""
        if "MCQ" in tool:
            prompt = f"Generate {num_items} multiple choice questions with answers from:\n{source[:3000]}"
        elif "Comparison" in tool:
            prompt = f"Compare {source} with features, pros, and cons in a table format."
        elif "Flashcard" in tool:
            prompt = f"Generate {num_items} flashcards (Question and Answer format) for:\n{source[:3000]}"
        elif "Formula" in tool:
            prompt = f"Generate a list of important formulas with explanations for:\n{source[:3000]}"
        elif "Mnemonic" in tool:
            prompt = f"Create a memorable mnemonic to remember the concepts in:\n{source[:3000]}"
            
        with st.spinner("Generating..."):
            reply = get_ai_reply(prompt)
            
        st.success("✅ Generated Successfully!")
        st.markdown(reply)
        
        st.download_button(
            label="📥 Download Result",
            data=reply,
            file_name=f"{tool.split()[1]}_result.txt",
            mime="text/plain",
            use_container_width=True
        )