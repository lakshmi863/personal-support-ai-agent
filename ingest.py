# ingest.py
from src.rag_pipeline import LocalRAGPipeline
import os

def main():
    # 1. Initialize the RAG Pipeline
    # This will point to the 'chroma_db' folder automatically
    rag = LocalRAGPipeline()

    # 2. Define the path to your data
    data_folder = "data"

    # 3. Check if data folder exists
    if not os.path.exists(data_folder):
        print(f"Error: The folder '{data_folder}' was not found. Please create it and add files.")
        return

    print(f"--- Starting Ingestion Process ---")
    print(f"Reading documents from: {data_folder}/")
    
    try:
        # 4. Run the ingestion
        rag.ingest_docs(data_folder)
        print(f"--- SUCCESS! ---")
        print(f"Your knowledge base is now stored in the 'chroma_db/' folder.")
        print(f"You can now run your chatbot using: streamlit run app.py")
    except Exception as e:
        print(f"--- ERROR DURING INGESTION ---")
        print(f"Details: {e}")

if __name__ == "__main__":
    main()