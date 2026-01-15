import streamlit as st
import requests
import json

st.set_page_config(page_title="RAG Chatbot", layout="centered")
st.title("🤖 RAG Chatbot")
st.markdown("AI-powered customer support")

# Get API key from Streamlit secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ Google API key not found. Please add it in Streamlit secrets.")
    st.stop()

# System prompt
SYSTEM_PROMPT = """You are a professional customer service AI assistant. Provide accurate, helpful, and friendly customer support. Keep responses concise and clear."""

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
                headers = {"Content-Type": "application/json"}
                data = {
                    "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\nUser: {prompt}"}]}],
                    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}
                }
                response = requests.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result["candidates"][0]["content"]["parts"][0]["text"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = f"Error: {response.status_code}"
                    st.error(error_msg)
                    st.info("💡 **Troubleshooting Tips:**\n1. Verify your API key is correct\n2. Enable 'Generative Language API' in Google Cloud Console\n3. Check API quota and billing settings")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Sidebar with minimal info
with st.sidebar:
    st.markdown("### About")
    st.markdown("Simple AI chatbot powered by Google Gemini")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
