import requests

def generate_stability_image(prompt, api_key, width="1024", height="1024",
                             cfg_scale=7, steps=30,
                             negative_prompt="blurry, low quality, ugly"):
    try:
        r = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image", # <-- Yahan comma lagaya gaya hai
            headers={
                "Authorization": f"Bearer {api_key}", 
                "Accept": "image/png", 
                "Content-Type": "application/json"
            },
            json={
                "text_prompts": [
                    {"text": prompt, "weight": 1.0}, 
                    {"text": negative_prompt, "weight": -1.0}
                ],
                "cfg_scale": cfg_scale, 
                "steps": steps, 
                "width": int(width), 
                "height": int(height), 
                "samples": 1
            },
            timeout=90
        )
        
        if r.status_code == 200:
            return {"success": True, "image": r.content}
        elif r.status_code == 402:
            return {"success": False, "error": "💰 Insufficient credits."}
        elif r.status_code == 401:
            return {"success": False, "error": "🔑 Invalid API key."}
        else:
            return {"success": False, "error": f"Error {r.status_code}: {r.text}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}