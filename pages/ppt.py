import streamlit as st
import os
from utils.ai import get_ai_reply
from utils.ppt_generator import generate_ppt, generate_html

def ppt_page():
    st.markdown("## 📊 PPT Generator")
    
    title = st.text_input("Presentation Title", placeholder="e.g., The Future of AI")
    num_slides = st.slider("Number of Slides", 2, 30, 5)
    
    # Details aur Button ko ek line mein lane ke liye
    col1, col2 = st.columns([4, 1])
    with col1:
        details = st.text_area("What should the presentation cover?", placeholder="e.g., Intro, Applications, Conclusion", height=100, label_visibility="collapsed")
    with col2:
        st.write("") 
        st.write("")
        st.write("")
        generate_btn = st.button("✨ Generate", type="primary", use_container_width=True)
    
    if generate_btn:
        if title and details:
            with st.spinner("Designing presentation..."):
                prompt = f"Create a detailed presentation outline for:\nTitle: {title}\nNumber of slides: {num_slides}\nTopics: {details}\n\nReturn format strictly:\nSlide 1: Title Here\nContent: Point 1\nContent: Point 2\n\nSlide 2: Title Here\nContent: Point 1"
                result = get_ai_reply(prompt)
                
                slides = []
                current_slide = {}
                
                for line in result.split('\n'):
                    line = line.strip()
                    if line.lower().startswith('slide') and ':' in line:
                        if current_slide:
                            slides.append(current_slide)
                        current_slide = {'title': line.split(':', 1)[1].strip(), 'content': ''}
                    elif line.lower().startswith('content') and ':' in line:
                        if current_slide:
                            content_part = line.split(':', 1)[1].strip()
                            current_slide['content'] += content_part + '\n'
                
                if current_slide:
                    slides.append(current_slide)
                    
                if not slides:
                    st.error("Failed to parse presentation structure. Try again.")
                    return
                    
                # Generate Files (Returns String paths)
                pptx_file = generate_ppt(title, slides)
                html_file = generate_html(title, slides)
                
                st.success("✅ Presentation generated successfully!")
                
                st.divider()
                st.markdown("### 📥 Downloads")
                
                c1, c2 = st.columns(2)
                if pptx_file and isinstance(pptx_file, str): # Fix for TypeError
                    with c1:
                        with open(pptx_file, "rb") as f:
                            st.download_button("📥 Download PPTX (PowerPoint)", f.read(), file_name=pptx_file, mime="application/vnd.openxmlformats-officedocument.presentationml.presentation", use_container_width=True)
                            
                if html_file and isinstance(html_file, str):
                    with c2:
                        with open(html_file, "r", encoding="utf-8") as f:
                            st.download_button("🌐 Download HTML (Browser)", f.read(), file_name=html_file, mime="text/html", use_container_width=True)
                            
                # Cleanup Server
                if pptx_file and os.path.exists(pptx_file): os.remove(pptx_file)
                if html_file and os.path.exists(html_file): os.remove(html_file)
        else:
            st.warning("Please enter a title and details.")
