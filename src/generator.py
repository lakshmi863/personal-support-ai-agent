import time
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, LLM_MODEL
from src.escalator import should_escalate, generate_handoff_summary 

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_response(user_query, persona_info, context_chunks):
    persona = persona_info['persona']
    
    # 1. Use the escalator logic (Check if we even need the LLM)
    escalate, reason = should_escalate(user_query, context_chunks)
    
    if escalate:
        return {
            "status": "ESCALATED",
            "response": "I'm connecting you with a human representative to assist with this specialized request.",
            "handoff_summary": generate_handoff_summary(user_query, persona, context_chunks, reason)
        }

    # 2. Generate response rules for Persona
    persona_rules = {
        "Technical Expert": "Tone: Deeply technical. Provide precise documentation references and structured steps.",
        "Frustrated User": "Tone: Extremely empathetic. Start by validating their experience/frustration. Provide clear, bolded instructions.",
        "Business Executive": "Tone: High-level, concise, and professional. Focus on ROI, timelines, and resolution impact."
    }

    context_text = "\n".join([f"Source ({c['source']}): {c['text']}" for c in context_chunks])
    
    system_prompt = (
        f"YOU ARE A CUSTOMER SUPPORT AGENT. YOUR CURRENT PERSONA RULES: {persona_rules[persona]}\n\n"
        f"STRICT RULE: ANSWER USING ONLY THIS CONTEXT:\n{context_text}\n\n"
        "If the answer is not in the context, say: 'I apologize, I do not have specific info on that, let me find a specialist.'"
    )

    # 3. GENERATION WITH RETRY LOGIC (to bypass 503/429 errors)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=LLM_MODEL,
                contents=user_query,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.2  # Low temperature for factual RAG responses
                )
            )

            return {
                "status": "SUCCESS",
                "response": response.text,
                "handoff_summary": None
            }

        except Exception as e:
            # Check for Service Unavailable (503) or Rate Limit (429)
            if ("503" in str(e) or "429" in str(e)) and attempt < max_retries - 1:
                # Exponential backoff: Wait 3s, then 6s
                wait_time = (attempt + 1) * 3
                print(f"⚠️ Model busy or quota hit. Retrying in {wait_time}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
                # If it's a different error or we ran out of retries, raise it
                raise e