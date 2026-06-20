import streamlit as st
import time
import os

# --- 1. PAGE CONFIGURATION (Absolute First Command) ---
st.set_page_config(
    page_title="Adsparkx AI Support", 
    layout="wide", 
    page_icon="🤖"
)

# --- 2. MULTI-USER PERFORMANCE CACHE ---
# Using cache_resource allows all users to share one instance of the RAG Database.
# This prevents the "blank screen" for 2nd/3rd users and saves RAM.
@st.cache_resource
def get_rag_pipeline():
    # Lazy import to speed up the UI shell rendering
    from src.rag_pipeline import LocalRAGPipeline
    return LocalRAGPipeline()

# --- 3. IMMEDIATE UI SHELL (Prevents White Screen) ---
header_col1, header_col2 = st.columns([1, 8])

with header_col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        st.write("🤖") 

with header_col2:
    st.title("Adaptive AI Support Agent")
    st.caption("Cross-Industry Intelligence Powered by Adsparkx.")

# --- 4. TOP NAVIGATION (Requested Industries) ---
service_tabs = st.tabs([
    "💻 SaaS Product Services", 
    "🛒 E-commerce Services", 
    "🛡️ IT Helpdesk Cloud Services", 
    "🏦 Banking Services", 
    "📱 Telecom Services"
])

# Interactive descriptions for each service tab
with service_tabs[0]: st.caption("Billing cycles, feature upgrades, and software account management.")
with service_tabs[1]: st.caption("Returns policy, shipping logistics, and order status tracking.")
with service_tabs[2]: st.caption("Cloud infrastructure, VM management, networking, and firewall rules.")
with service_tabs[3]: st.caption("Fraud reports, transaction limits, EMI details, and account security.")
with service_tabs[4]: st.caption("Broadband setup, MNP portability, 5G signal issues, and plan recharges.")

st.markdown("---")

# Placeholder for visible startup loading (runs only once per browser session)
startup_placeholder = st.empty()

# --- 5. INITIALIZATION (Multi-User Safe) ---
# Import modules only when needed
from src.classifier import classify_customer_persona
from src.generator import generate_response

if "rag" not in st.session_state:
    with startup_placeholder.container():
        with st.status("Connecting to Knowledge Base...", expanded=True) as status:
            st.write("Accessing sector-specific documentation...")
            # Initializes or gets the shared RAG engine
            st.session_state.rag = get_rag_pipeline()
            
            st.write("Handshaking with Adsparkx AI Response Engine...")
            time.sleep(0.5) 
            
            status.update(label="All Industries Loaded!", state="complete", expanded=False)
            time.sleep(0.5)
    startup_placeholder.empty()

# Initialize Private Session States
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_persona" not in st.session_state:
    st.session_state.current_persona = "Unknown"

# --- 6. SIDEBAR SETUP ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    
    st.header("👤 Agent Status")
    persona_display = st.empty()
    persona_display.metric("Detected Persona", st.session_state.current_persona)
    
    st.markdown("---")
    st.info("""
    **Enterprise Intelligence:**
    - Detects Sentiment & Industry Context.
    - Persona-Adaptive Tone Shift.
    - Grounded Truth (Zero Hallucinations).
    - Policy-Compliant Human Escalation.
    """)
    
    if st.button("Clear Private Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_persona = "Unknown"
        st.rerun()

# --- 7. PRIVATE CHAT RENDERING ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 8. AI ADAPTIVE LOGIC ---
if prompt := st.chat_input("How can I help you today?"):
    
    # Store user query in their private session history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process AI Assistant Response
    with st.chat_message("assistant"):
        # Real-time progress updates via Checklist
        with st.status("Analyzing and Searching Knowledge Base...", expanded=True) as status:
            try:
                # Step 1: Detect Tone/Sentiment
                st.write("Identifying persona and industry sector...")
                persona_data = classify_customer_persona(prompt)
                st.session_state.current_persona = persona_data['persona']
                persona_display.metric("Detected Persona", st.session_state.current_persona)

                # Step 2: Retrieve Relevant Policies
                st.write("Finding specific support documentation...")
                context = st.session_state.rag.retrieve(prompt)

                # Step 3: Draft Tone-Shifted Response
                st.write("Drafting Expert Response...")
                result = generate_response(prompt, persona_data, context)
                
                status.update(label="Reasoning Complete!", state="complete", expanded=False)

            except Exception as e:
                status.update(label="Processing Error", state="error")
                st.error(f"Something failed during generation: {e}")
                st.stop()

        # Final UI Presentation (Human Escalation or Simulated Stream)
        if result["status"] == "ESCALATED":
            st.warning("Specialized query: Connecting you to a Human Professional.")
            st.markdown(result["response"])
            with st.expander("Escalation Data Package"):
                st.json(result["handoff_summary"])
            final_out = result["response"]
        else:
            # Word-by-word simulated streaming
            placeholder = st.empty()
            stream_text = ""
            for word in result["response"].split():
                stream_text += word + " "
                time.sleep(0.04) 
                placeholder.markdown(stream_text + "▌")
            placeholder.markdown(result["response"])
            final_out = result["response"]

        # Context Attribution
        if context:
            with st.expander("Knowledge Base References (Sources)"):
                for c in context:
                    st.write(f"**Document:** {c['source']} (Match Rank: {c['score']:.2f})")
                    st.caption(f"{c['text'][:300]}...")

        # Persist response in private session
        st.session_state.messages.append({"role": "assistant", "content": final_out})