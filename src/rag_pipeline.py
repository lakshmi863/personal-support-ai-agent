import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
import chromadb
from src.config import GEMINI_API_KEY, EMBEDDING_MODEL, CHROMA_DB_DIR, CHUNK_SIZE, CHUNK_OVERLAP

client = genai.Client(api_key=GEMINI_API_KEY)

class LocalRAGPipeline:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.collection = self.chroma_client.get_or_create_collection(name="support_kb")

    def get_embedding(self, text: str) -> list:
        """Calls Gemini API to convert text into a mathematical vector."""
        response = client.models.embed_content(model=EMBEDDING_MODEL, contents=text)
        return response.embeddings[0].values

    def ingest_docs(self, data_dir: str):
        """Reads all files in data_dir, chunks them, and adds them to ChromaDB with error handling."""
        splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        
        if not os.path.exists(data_dir):
            print(f"❌ Error: Data directory '{data_dir}' not found.")
            return

        print(f"--- Starting Ingestion from: {data_dir} ---")

        for filename in os.listdir(data_dir):
            path = os.path.join(data_dir, filename)
            content = ""
            
            if os.path.isdir(path):
                continue

            try:
                # 1. Extract Text based on file extension
                if filename.endswith(".txt") or filename.endswith(".md"):
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()

                elif filename.endswith(".pdf"):
                    try:
                        from pypdf import PdfReader
                        reader = PdfReader(path)
                        for page in reader.pages:
                            page_text = page.extract_text()
                            if page_text:                   # ✅ inside the loop
                                content += page_text + "\n"
                    except Exception as pdf_error:
                        print(f"⚠️ Skipping corrupted PDF {filename}: {pdf_error}")
                        continue

                # 2. Safety Check: Skip empty or unreadable files
                if not content.strip():
                    print(f"⚠️ Skipping empty or unreadable file: {filename}")
                    continue

                # 3. Chunking and Vectorization
                chunks = splitter.split_text(content)
                for idx, chunk in enumerate(chunks):
                    embedding = self.get_embedding(chunk)
                    chunk_id = f"{filename}_{idx}"
                    
                    self.collection.add(
                        ids=[chunk_id],
                        embeddings=[embedding],
                        metadatas=[{"source": filename}],
                        documents=[chunk]
                    )
                print(f"✅ Successfully ingested: {filename}")

            except Exception as e:
                print(f"❌ Failed to process {filename}: {e}")

        print(f"--- Ingestion Complete ---")

    def retrieve(self, query: str, k: int = 3):
        """Performs a semantic similarity search in the Vector DB."""
        query_vector = self.get_embedding(query)
        
        results = self.collection.query(query_embeddings=[query_vector], n_results=k)
        
        retrieved_data = []
        if results and results['documents']:
            for i in range(len(results['documents'][0])):
                dist = results['distances'][0][i] if results['distances'] else 0
                similarity = 1.0 - dist
                
                retrieved_data.append({
                    "text": results['documents'][0][i],
                    "source": results['metadatas'][0][i]['source'],
                    "score": similarity
                })
        return retrieved_data