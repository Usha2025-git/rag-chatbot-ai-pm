import streamlit as st
import requests
import json

st.set_page_config(page_title="RAG Chatbot", layout="centered")
st.title("🤖 RAG Chatbot")
st.markdown("AI-powered customer support")

# Get API key from Streamlit secrets
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("⚠️ Groq API key not found. Please add it in Streamlit secrets.")
    st.stop()

# System prompt
SYSTEM_PROMPT = "You are a professional customer service AI assistant. Provide accurate, helpful, and friendly customer support. Keep responses concise and clear."

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
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Sidebar with minimal info
with st.sidebar:
    st.markdown("### About")
    st.markdown("Simple AI chatbot powered by Groq (Llama 3.3)")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
