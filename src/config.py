import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LLM_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "gemini-embedding-001"

CHROMA_DB_DIR = "./chroma_db"
CHUNK_SIZE = 600
CHUNK_OVERLAP = 80

CONFIDENCE_THRESHOLD = 0.35
SENSITIVE_TOPICS = ["refund", "legal", "lawsuit", "cancel account", "payment info"]