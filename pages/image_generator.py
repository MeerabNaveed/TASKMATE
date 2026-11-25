import os
import streamlit as st
from io import BytesIO
from datetime import datetime
from PIL import Image
from dotenv import load_dotenv
from utils.image_gen import generate_stability_image

load_dotenv()

def image_page():
    st.markdown("## 🖼️ AI Image Generator")
    
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        api_key = st.text_input("🔑 Stability AI API Key", type="password", help="Get it from platform.stability.ai")
        if not api_key:
            st.warning("API Key required to generate images.")
            return

    # Input Box aur Button ko ek line mein lane ke liye
    col1, col2 = st.columns([4, 1])
    
    with col1:
        prompt = st.text_area("Describe the image", placeholder="e.g., A futuristic city with neon lights...", label_visibility="collapsed", height=80)
    
    with col2:
        st.write("") # Alignment spacing
        st.write("")
        generate_btn = st.button("🎨 Generate", type="primary", use_container_width=True)

    # Styles aur Settings
    c1, c2, c3 = st.columns(3)
    with c1:
        style = st.selectbox("Style", ["photorealistic", "anime", "digital art", "cinematic", "3d render", "oil painting", "watercolor", "sketch", "cyberpunk", "fantasy"])
    with c2:
        width = st.selectbox("Width", ["512", "768", "1024"], index=2)
    with c3:
        height = st.selectbox("Height", ["512", "768", "1024"], index=2)

    if generate_btn:
        if not prompt:
            st.warning("Please enter an image description.")
            return
            
        final_prompt = f"{prompt}, {style}, high quality, detailed"
        
        with st.spinner("Generating image..."):
            result = generate_stability_image(
                prompt=final_prompt,
                api_key=api_key,
                width=int(width), 
                height=int(height)
            )
            
        if result["success"]:
            image = Image.open(BytesIO(result["image"]))
            st.image(image, caption=prompt, use_container_width=True)
            
            img_bytes = BytesIO()
            image.save(img_bytes, format='PNG')
            
            st.download_button(
                label="📥 Download Image",
                data=img_bytes.getvalue(),
                file_name=f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png",
                use_container_width=True
            )
            st.success("✅ Image generated successfully!")
        else:
            st.error(result["error"])
   