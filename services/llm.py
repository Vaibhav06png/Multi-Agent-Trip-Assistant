import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API key missing")

genai.configure(api_key=api_key)


def call_gemini(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-3.1-flash-lite") 
    response = model.generate_content(prompt)
    return response.text.strip()