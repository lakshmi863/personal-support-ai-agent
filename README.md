Persona-Adaptive AI Support Agent (Adsparkx)

A state-of-the-art Retrieval-Augmented Generation (RAG) customer support system built with Python, Streamlit, ChromaDB, and Google Gemini Pro. This agent doesn't just answer questions—it detects the user's "persona" and shifts its tone to match, providing a highly personalized support experience.

web site url( https://personal-support-ai-agent.onrender.com )

Features

Persona-Adaptive Responses: Automatically classifies users into three personas:
Technical Expert: Precise, technical, and step-oriented.
Frustrated User: Highly empathetic and validating.
Business Executive: Concise, professional, and focused on resolution impact.

Local RAG Pipeline: Ingests your own .pdf, .md, and .txt documentation into a persistent vector database (ChromaDB) for factual answering.
Automated Escalation: Intelligent logic triggers a human representative handoff if the knowledge base confidence is low or if a sensitive topic (billing/legal) is detected.

Advanced UI Experience:

Instant Startup Loader: Shows system initialization status instead of a blank white screen.
Task Checklists: Shows live status as the AI thinks.
Typewriter Effect: Simulated streaming for a smoother chat experience.

Tech Stack

Frontend: Streamlit
AI Models: Google Gemini (Flash 2.0 / Pro) & Gemini Embeddings
Database: ChromaDB (Vector Search)
Frameworks: LangChain (Text Splitting), PyPDF

Installation & Setup

1. Clone the repository
code
Bash
git clone https://github.com/lakshmi863/personal-support-ai-agent.git
cd personal-support-ai-agent
2. Create a Virtual Environment
code
Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
code
Bash
pip install -r requirements.txt
4. Configuration
Create a .env file in the root directory and add your Google Gemini API Key:
code
Env
GEMINI_API_KEY="YOUR_API_KEY_HERE"

Data Ingestion

To feed the AI your support documents (manuals, policies, FAQs):
Place your files (.txt, .md, or .pdf) in the data/ folder.
Run the ingestion script:
code
Bash
python ingest.py
This will chunk your documents and store them as mathematical embeddings in the chroma_db/ folder.

Usage

Launch the AI support interface:
code
Bash
streamlit run app.py
The application will open in your browser at http://localhost:8501.

Project Structure

code
Text
persona-support-agent/

├── src/

│   ├── classifier.py   # Persona/Sentiment detection logic

│   ├── rag_pipeline.py # ChromaDB management & retrieval

│   ├── generator.py    # Gemini response generation

│   ├── escalator.py    # Human handoff logic

│   └── config.py       # Constants & Model settings

├── data/               # Your source PDF/MD/TXT documents

├── chroma_db/          # Persistent vector storage (auto-generated)

├── app.py              # Main Streamlit UI Application

├── ingest.py           # Document processing script

└── requirements.txt    # Project dependencies
