# list_models.py
import os
from google import genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print(" Error: No API key found. Check your .env file.")
else:
    client = genai.Client(api_key=api_key)
    print("--- Searching for available models ---")
    try:
        # List all models available to your API key
        for model in client.models.list():
            print(f"Found model: {model.name}")
    except Exception as e:
        print(f" An error occurred: {e}")