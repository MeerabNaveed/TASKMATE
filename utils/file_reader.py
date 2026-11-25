import pypdf
import docx
import pandas as pd

def read_uploaded_file(uploaded_file):
    try:
        name = uploaded_file.name.lower()
        
        if name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8", errors="ignore")
            
        elif name.endswith(".pdf"):
            reader = pypdf.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
            return text if text.strip() else None
            
        elif name.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            return "\n".join(p.text for p in doc.paragraphs)
            
        elif name.endswith(".csv"):
            return pd.read_csv(uploaded_file).to_string()
            
        elif name.endswith(".xlsx"):
            return pd.read_excel(uploaded_file).to_string()
            
        else:
            return uploaded_file.read().decode("utf-8", errors="ignore")
            
    except Exception as e:
        return f"Error: {e}"