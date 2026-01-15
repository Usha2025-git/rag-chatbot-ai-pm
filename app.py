import streamlit as st
import requests
import json
import anthropic
import google.generativeai as genai
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="🤖 RAG Chatbot - AI PM Portfolio",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {text-align: center; padding: 1rem 0;}
    .stChatMessage {border-radius: 15px;}
    .cost-badge {background: #f0f2f6; padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🤖 RAG Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;">AI PM Case Study: Multi-Model Customer Support Automation</p>', unsafe_allow_html=True)

# Sidebar - Model Selection and Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model selection
    model_provider = st.selectbox(
        "Select AI Provider",
        ["Groq (Free)", "Claude (Anthropic)", "GPT-4 (OpenAI)", "Gemini (Google)"],
        help="Choose your preferred AI model provider"
    )
    
    # Model info
    model_info = {
        "Groq (Free)": {"model": "llama-3.3-70b-versatile", "cost": "FREE", "latency": "0.4s"},
        "Claude (Anthropic)": {"model": "claude-3-5-sonnet-20241022", "cost": "$0.60/1K", "latency": "1.2s"},
        "GPT-4 (OpenAI)": {"model": "gpt-4o", "cost": "$0.90/1K", "latency": "0.8s"},
        "Gemini (Google)": {"model": "gemini-1.5-pro", "cost": "$0.30/1K", "latency": "1.5s"}
    }
    
    info = model_info[model_provider]
    st.markdown(f"""
    <div class="cost-badge">
        <b>Model:</b> {info['model']}<br>
        <b>Est. Cost:</b> {info['cost']}<br>
        <b>Avg Latency:</b> {info['latency']}
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### About This Project")
    st.markdown("""
    This chatbot demonstrates **AI Product Management** skills:
    - 🧠 Multi-model evaluation
    - 📊 Cost/latency tradeoffs
    - 🛡️ Error handling & guardrails
    - 🎨 Production-ready UX
    """)
    
    st.divider()
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# System prompt
SYSTEM_PROMPT = """You are a professional customer service AI assistant. Provide accurate, helpful, and friendly customer support. Keep responses concise and clear. If you don't know something, say so honestly and offer to escalate to a human agent."""

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("💬 Ask me anything about our products or services..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response based on selected provider
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = None
                
                # GROQ API
                if model_provider == "Groq (Free)":
                    try:
                        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
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
                        response = requests.post(url, headers=headers, json=data, timeout=30)
                        if response.status_code == 200:
                            result = response.json()
                            answer = result["choices"][0]["message"]["content"]
                        else:
                            st.error(f"Groq API error: {response.status_code}")
                    except KeyError:
                        st.error("⚠️ Groq API key not found. Please add GROQ_API_KEY to Streamlit secrets.")
                
                # CLAUDE API
                elif model_provider == "Claude (Anthropic)":
                    try:
                        CLAUDE_API_KEY = st.secrets["CLAUDE_API_KEY"]
                        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
                        message = client.messages.create(
                            model="claude-3-5-sonnet-20241022",
                            max_tokens=1024,
                            system=SYSTEM_PROMPT,
                            messages=[
                                {"role": "user", "content": prompt}
                            ]
                        )
                        answer = message.content[0].text
                    except KeyError:
                        st.error("⚠️ Claude API key not found. Please add CLAUDE_API_KEY to Streamlit secrets.")
                
                # OPENAI API
                elif model_provider == "GPT-4 (OpenAI)":
                    try:
                        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
                        client = OpenAI(api_key=OPENAI_API_KEY)
                        completion = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=1024
                        )
                        answer = completion.choices[0].message.content
                    except KeyError:
                        st.error("⚠️ OpenAI API key not found. Please add OPENAI_API_KEY to Streamlit secrets.")
                
                # GEMINI API
                elif model_provider == "Gemini (Google)":
                    try:
                        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
                        genai.configure(api_key=GEMINI_API_KEY)
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {prompt}\n\nAssistant:"
                        response = model.generate_content(full_prompt)
                        answer = response.text
                    except KeyError:
                        st.error("⚠️ Gemini API key not found. Please add GEMINI_API_KEY to Streamlit secrets.")
                
                # Display answer
                if answer:
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.warning("🤔 No response generated. Please check your API keys.")
                    
            except requests.exceptions.Timeout:
                st.error("⏰ Request timed out. Please try again.")
            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")
                st.info("👋 Need help? Our human support team is available 24/7. Type 'speak to agent' to escalate.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8em;">
    📦 <b>AI PM Portfolio Project</b> | Built with Streamlit | 
    <a href="https://github.com/Usha2025-git/rag-chatbot-ai-pm" target="_blank">View Source</a>
</div>
""", unsafe_allow_html=True)
