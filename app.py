import streamlit as st
import time
import os
from src.classifier import classify_customer_persona
from src.rag_pipeline import LocalRAGPipeline
from src.generator import generate_response

# --- 1. PAGE CONFIGURATION ---
# This must be the very first Streamlit command to prevent errors
st.set_page_config(
    page_title="Adsparkx AI Support", 
    layout="wide", 
    page_icon="🤖"
)

# --- 2. INITIAL UI HEADER (Renders Instantly) ---
# This ensures the user sees the Title and Logo immediately
header_col1, header_col2 = st.columns([1, 8])

with header_col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        st.write("") # Fallback icon if logo.png is missing

with header_col2:
    st.title("Adaptive AI Support Agent")
    st.caption("AI-Powered Support tailored to your sentiment and technical expertise.")

st.markdown("---")

# Placeholder for the system initialization status
startup_placeholder = st.empty()

# --- 3. SYSTEM BOOTSTRAPPER (Initialization) ---
# Fixes the white screen by providing visible feedback on startup
if "rag" not in st.session_state:
    with startup_placeholder.container():
        with st.status("System Initializing...", expanded=True) as setup_status:
            st.write("Accessing Vector Database (ChromaDB)...")
            # Connecting to Local Knowledge Base
            st.session_state.rag = LocalRAGPipeline()
            
            st.write("Connecting to Adsparkx AI Response Engine...")
            time.sleep(0.5) 
            
            st.write("✨ Done! System is live.")
            setup_status.update(label="Initialization Complete!", state="complete", expanded=False)
            time.sleep(0.8) # Brief pause for smooth transition
    startup_placeholder.empty()

# Initialize Conversation States
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_persona" not in st.session_state:
    st.session_state.current_persona = "Unknown"

# --- 4. SIDEBAR CONFIGURATION ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    
    st.header("Agent Status")
    persona_display = st.empty()
    persona_display.metric("Detected Persona", st.session_state.current_persona)
    
    st.markdown("---")
    st.info("""
    **Intelligence Level:**
    - Detects **Persona** (Technical vs Business).
    - Identifies **Sentiment** (Frustrated vs Calm).
    - Adjusts **Tone** and **Policies** dynamically.
    """)
    
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_persona = "Unknown"
        st.rerun()

# --- 5. CHAT HISTORY RENDERING ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. MAIN CHAT INPUT & AI LOGIC ---
if prompt := st.chat_input("How can I help you today?"):
    
    # A. Display User Question
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # B. Generate Assistant Response
    with st.chat_message("assistant"):
        # Checklist-style loading
        with st.status("Analyzing and Searching...", expanded=True) as status:
            try:
                # STEP 1: Classifier
                st.write("Identifying user persona and sentiment...")
                persona_data = classify_customer_persona(prompt)
                st.session_state.current_persona = persona_data['persona']
                persona_display.metric("Detected Persona", st.session_state.current_persona)

                # STEP 2: RAG Pipeline
                st.write("Scanning knowledge base documents...")
                context = st.session_state.rag.retrieve(prompt)

                # STEP 3: Response Generation
                st.write("Creating personalized response...")
                result = generate_response(prompt, persona_data, context)
                
                status.update(label="Thinking Complete!", state="complete", expanded=False)

            except Exception as e:
                status.update(label="System Error", state="error")
                st.error(f"Logic failure: {e}")
                st.stop()

        # C. DISPLAYING FINAL OUTPUT (With Typewriter Streaming)
        if result["status"] == "ESCALATED":
            st.warning("CRITICAL: Human Handoff Initiated")
            st.markdown(result["response"])
            with st.expander("Escalation Metadata (For Humans)"):
                st.json(result["handoff_summary"])
            final_content = result["response"]
        else:
            # Typing Simulation
            placeholder = st.empty()
            full_typed_text = ""
            # Breaking response into words for simulated stream
            for word in result["response"].split():
                full_typed_text += word + " "
                time.sleep(0.04) # Speed of typewriter
                placeholder.markdown(full_typed_text + "▌")
            placeholder.markdown(result["response"])
            final_content = result["response"]

        # D. RETRIEVED SOURCES (Transparent Support)
        if context:
            with st.expander("Sources Cited"):
                for c in context:
                    st.write(f"**{c['source']}** (Match Score: {c['score']:.2f})")
                    st.caption(f"{c['text'][:300]}...")

        # Store in session state for persistency
        st.session_state.messages.append({"role": "assistant", "content": final_content})