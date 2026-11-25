import streamlit as st
from utils.speech import text_to_speech_bytes

def voice_page():
    st.markdown("## 🎙️ Voice Assistant")
    
    tab1, tab2 = st.tabs(["🎤 Speech to Text", "🔊 Text to Speech"])
    
    with tab1:
        st.info("🎙️ Click the button below and allow microphone access to speak.")
        
        try:
            from streamlit_mic_recorder import speech_to_text
            text = speech_to_text(
                language='en',
                use_container_width=True,
                just_once=False,
                key='STT'
            )
            
            if text:
                st.success("📝 Transcribed Text:")
                st.text_area("Result", text, height=100)
        except ImportError:
            st.error("Please install `streamlit-mic-recorder` to use this feature. Run: `pip install streamlit-mic-recorder`")
            
    with tab2:
        text_input = st.text_area("Enter text to convert to speech", height=150, placeholder="Type something here...")
        
        if st.button("🔊 Generate Speech", type="primary", use_container_width=True):
            if text_input:
                with st.spinner("Generating audio..."):
                    audio_bytes = text_to_speech_bytes(text_input)
                    
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button(
                        label="📥 Download Audio",
                        data=audio_bytes,
                        file_name="speech.mp3",
                        mime="audio/mpeg"
                    )
                else:
                    st.error("Failed to generate audio.")
            else:
                st.warning("Please enter some text.")