import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception:
    client = None

MODEL_NAME = "gemini-3.6-flash"

def get_ai_reply(user_input, context=""):
    if client is None:
        return "⚠️ AI client not initialized. Check GEMINI_API_KEY."
    
    # Chat memory add ki gayi hai
    prompt = context + f"\nUser: {user_input}" if context else user_input
    
    for attempt in range(3):
        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
            return response.text
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
            else:
                return f"⚠️ AI Error: {e}"
    return "⚠️ Unknown error."