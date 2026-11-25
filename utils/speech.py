from gtts import gTTS
from io import BytesIO

def text_to_speech_bytes(text):
    try:
        tts = gTTS(text=text, lang="en")
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.getvalue()
    except Exception:
        return None