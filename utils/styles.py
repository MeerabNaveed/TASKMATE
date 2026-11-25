import base64
import streamlit as st

def get_logo_base64():
    try:
        with open("image.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

LOGO_BASE64 = get_logo_base64()

def inject_css():
    st.markdown("""
    <style>
        /* App Background */
        .stApp { background: linear-gradient(135deg, #0a0a1a, #14142b, #0a0a1a); }
        
        /* Headings Gradient */
        h2 { 
            background: linear-gradient(135deg, #6C63FF, #FF6584);
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
        } 
        
        /* Buttons Styling */
        .stButton > button {
            background: linear-gradient(135deg, #6C63FF, #FF6584) !important;
            color: white !important; 
            border-radius: 8px !important; 
            border: none !important; 
            width: 100% !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
        }
        
        /* Cards Styling */
        .card { 
            background: rgba(255,255,255,0.04); 
            border-radius: 16px;
            padding: 1.5rem; 
            border: 1px solid rgba(255,255,255,0.05); 
        }
        
        /* Metric Cards */
        .metric-card { 
            background: rgba(255,255,255,0.04); 
            border-radius: 16px;
            padding: 1.5rem; 
            text-align: center; 
            border: 1px solid rgba(255,255,255,0.05);
        }
        
        /* Metric Value Text */
        .metric-value { 
            font-size: 2.2rem; 
            font-weight: 700; 
            background: linear-gradient(135deg, #6C63FF, #FF6584);
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
        }
        
        /* Chat Bubbles */
        .user-bubble { 
            background: linear-gradient(135deg, #6C63FF, #FF6584);
            color: white; 
            border-radius: 18px 18px 4px 18px;
            padding: 0.75rem 1.25rem; 
            margin: 0.5rem 0;
            max-width: 80%; 
            float: right; 
        }
        
        .assistant-bubble { 
            background: rgba(255,255,255,0.06);
            color: white; 
            border-radius: 18px 18px 18px 4px;
            padding: 0.75rem 1.25rem; 
            margin: 0.5rem 0;
            max-width: 80%; 
            float: left; 
            border: 1px solid rgba(255,255,255,0.05);
        }
    </style>
    """, unsafe_allow_html=True)