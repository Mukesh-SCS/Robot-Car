import openai
import os
import base64

# First try env var, then file:
key = os.getenv("OPENAI_API_KEY")
if not key:
    key_file = os.path.expanduser("~/.config/openai/api_key")
    if not os.path.exists(key_file):
        raise FileNotFoundError("OpenAI API key not found in environment variable or at ~/.config/openai/api_key")
    with open(key_file) as f:
        key = f.read().strip()
openai.api_key = key

def ask_gpt(prompt: str, image_path: str = None) -> str:
    """
    Send text (and optional image) to ChatGPT and return its reply.
    """
    messages = [{"role": "user", "content": prompt}]
    if image_path:
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        messages.append({
            "role": "user",
            "content": f"<image>{b64}</image>\n\nWhat do you see?"
        })

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.5,
            max_tokens=150
        )
        return resp.choices[0].message.content.strip()
    except openai.error.OpenAIError as e:
        return f"API error: {e}"
    


    #### import os, openai
#####openai.api_key = os.getenv("OPENAI_API_KEY")

    ### export OPENAI_API_KEY="sk-··········"
