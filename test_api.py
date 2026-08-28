"""Minimal test to confirm the Gemini API key in .env works.

Run with:
    .venv/bin/python test_api.py

This loads .env, verifies the required variables are present, and makes a
single tiny generate_content call so you know the key is valid before trying
the full interactive chat.
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

model = os.getenv("GEMINI_MODEL", "")
api_key = os.getenv("GEMINI_API_KEY", "")

assert model, "Error: GEMINI_MODEL cannot be empty. Update .env"
assert api_key, "Error: GEMINI_API_KEY cannot be empty. Update .env"

print(f"Loaded model: {model!r}")
print(f"Loaded API key: {api_key[:8]}... (length={len(api_key)})")

client = genai.Client(api_key=api_key)

print("\nMaking a minimal test call...")
response = client.models.generate_content(
    model=model,
    contents="Say 'OK'",
)

print("\nResponse received:")
print(response.text)
