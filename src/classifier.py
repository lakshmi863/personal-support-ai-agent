import os, json, time
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, LLM_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)

def classify_customer_persona(user_message: str) -> dict:
    # --- ADDED RETRY LOGIC ---
    max_retries = 3
    for attempt in range(max_retries):
        try:
            system_instruction = (
                "Analyze message and return JSON: {'persona': 'Technical Expert'|'Frustrated User'|'Business Executive', "
                "'is_sensitive': bool, 'reasoning': 'string'}"
            )

            schema = {
                "type": "OBJECT",
                "properties": {
                    "persona": {"type": "STRING", "enum": ["Technical Expert", "Frustrated User", "Business Executive"]},
                    "is_sensitive": {"type": "BOOLEAN"},
                    "reasoning": {"type": "STRING"}
                },
                "required": ["persona", "is_sensitive", "reasoning"]
            }

            response = client.models.generate_content(
                model=LLM_MODEL,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.1
                )
            )
            return json.loads(response.text)
        
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                time.sleep(5) # Wait 5 seconds and try again
                continue
            raise e