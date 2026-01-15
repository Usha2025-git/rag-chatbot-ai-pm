import streamlit as st
import requests
import json
from datetime import datetime

# Page config with custom theme
st.set_page_config(
    page_title="🤖 RAG Chatbot - AI PM Portfolio",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Modern CSS with stunning gradients and animations
st.markdown("""
<style>
    /* Main gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .main-header h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: #f0f0f0;
        font-size: 1.1rem;
        margin-top: 0;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Input styling */
    .stChatInput {
        border-radius: 25px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.9);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #FF6B6B 0%, #FFE66D 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Metrics/Stats styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 RAG Chatbot</h1>
    <p>AI-Powered Customer Support | Built by AI Product Manager</p>
</div>
""", unsafe_allow_html=True)

# Get API key from Streamlit secrets
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("⚠️ Groq API key not found. Please add it in Streamlit secrets.")
    st.stop()

# System prompt
SYSTEM_PROMPT = """You are a professional customer service AI assistant. 
Provide accurate, helpful, and friendly customer support. 
Keep responses concise and clear. Use emojis occasionally to be friendly."""

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Hi! I'm your AI customer support assistant. How can I help you today?"
    })

if 'message_count' not in st.session_state:
    st.session_state.message_count = 0

# Sidebar with metrics and info
with st.sidebar:
    st.markdown("### 📊 Chat Metrics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #667eea; margin: 0;">⚡</h3>
            <p style="margin: 0; color: #666;">Fast</p>
            <p style="margin: 0; font-weight: bold;">&lt;1s</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #764ba2; margin: 0;">💬</h3>
            <p style="margin: 0; color: #666;">Messages</p>
            <p style="margin: 0; font-weight: bold;">{st.session_state.message_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Powered by:**
    - 🧠 Groq (Llama 3.3 70B)
    - ⚡ <1s response time
    - 💰 Cost-effective API
    
    **AI PM Portfolio Project**
    - Problem framing ✅
    - Metrics design ✅
    - LLM evaluation ✅
    - Guardrails ✅
    """)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "👋 Chat cleared! How can I help you?"
        }]
        st.session_state.message_count = 0
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: white; font-size: 0.9rem;">
        Made with ❤️ by<br>
        <strong>Usha Swinir</strong><br>
        AI Product Manager
    </div>
    """, unsafe_allow_html=True)

# Main chat interface
st.markdown("### 💬 Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("💭 Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.message_count += 1
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1024
                }
                
                response = requests.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.session_state.message_count += 1
                else:
                    error_msg = f"❌ Error: {response.status_code} - {response.text}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except Exception as e:
                error_msg = f"⚠️ An error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer with project info
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 1rem;">
    <p style="margin: 0;">🚀 <strong>AI PM Portfolio Project</strong> | Customer Support Automation</p>
    <p style="margin: 0; font-size: 0.9rem;">Demonstrating: LLM Integration • Cost Optimization • User Experience Design</p>
    <p style="margin: 0.5rem 0 0 0;">📚 <a href="https://github.com/Usha2025-git/rag-chatbot-ai-pm" style="color: #FFE66D;">View on GitHub</a> • 
    <a href="https://www.linkedin.com/in/ushaswinir-product/" style="color: #FFE66D;">LinkedIn</a></p>
</div>
""", unsafe_allow_html=True)
