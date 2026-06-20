import json
from src.config import CONFIDENCE_THRESHOLD, SENSITIVE_TOPICS

def should_escalate(query, context_chunks):
    """
    Checks if the query requires a human.
    Returns: (True/False, reason_string)
    """
    # 1. Check Retrieval Confidence
    best_score = max([c['score'] for c in context_chunks]) if context_chunks else 0
    
    # 2. Check for Sensitive Topics (Billing/Legal)
    is_sensitive = any(topic in query.lower() for topic in SENSITIVE_TOPICS)

    if is_sensitive:
        return True, "Sensitive Topic detected."
    
    if best_score < CONFIDENCE_THRESHOLD:
        return True, "Insufficient Knowledge found."
        
    return False, None

def generate_handoff_summary(query, persona, chunks, reason):
    """Generates the required structured JSON for human agents."""
    return {
        "status": "Escalated to Human",
        "reason": reason,
        "metadata": {
            "persona_detected": persona,
            "query": query,
            "policy_found": chunks[0]['text'][:200] if chunks else "No specific policy found",
            "sources_checked": list(set([c['source'] for c in chunks])),
            "next_step": "Investigate backend logs and contact user."
            
        }
    }