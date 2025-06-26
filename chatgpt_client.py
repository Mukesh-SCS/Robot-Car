# chatgpt_client.py
import openai
import os
import base64

# Load your key from file
api_key_path = os.path.expanduser("~/.config/openai/api_key")
if not os.path.exists(api_key_path):
    raise RuntimeError(f"OpenAI API key file not found at {api_key_path}")
openai.api_key_path = api_key_path

def ask_gpt(prompt: str, image_path: str = None) -> str:
    """
    Send a text (and optional image) to ChatGPT and return its reply.
    """
    messages = [{"role": "user", "content": prompt}]

    if image_path:
        # Read and base64-encode the image
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        # Embedding image as text (not officially supported)
        messages.append({
            "role": "user",
            "content": f"<image>{b64}</image>\n\nWhat do you see?"
        })

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # or "gpt-4v" if you have Vision
            messages=messages,
            temperature=0.5,
            max_tokens=150
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI API error: {e}"
