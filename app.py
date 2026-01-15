import streamlit as st
import requests
import json

st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("🤖 RAG Chatbot Platform")
st.markdown("AI-powered customer support using Google Gemini AI")

# Get API key from Streamlit secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ Google API key not found. Please add it in Streamlit secrets.")
    st.stop()

# System prompt for better responses
SYSTEM_PROMPT = """You are a professional customer service AI assistant.

YOUR ROLE:
- Provide accurate, helpful, and friendly customer support
- Answer questions about products, services, and policies
- Maintain a warm, professional, and empathetic tone

GUIDELINES:
- Keep responses concise and clear
- If you don't know something, be honest and offer to escalate
- Always end with "Is there anything else I can help you with?"

TONE: Friendly, professional, empathetic
"""

# Sidebar settings
st.sidebar.header("⚙️ Settings")
model_type = st.sidebar.selectbox("Select Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)

# Tabs
tab1, tab2, tab3 = st.tabs(["Chat", "Analytics", "Documentation"])

with tab1:
    st.subheader("💬 Chat Interface")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Your question:"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Call Google Gemini API
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_type}:generateContent?key={GOOGLE_API_KEY}"
                    
                    # Build conversation context
                    full_prompt = f"{SYSTEM_PROMPT}\n\nCustomer question: {prompt}"
                    
                    headers = {"Content-Type": "application/json"}
                    data = {
                        "contents": [{
                            "parts": [{"text": full_prompt}]
                        }],
                        "generationConfig": {
                            "temperature": temperature,
                            "maxOutputTokens": 2048
                        }
                    }
                    
                    response = requests.post(url, headers=headers, json=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        answer = result["candidates"][0]["content"]["parts"][0]["text"]
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        error_msg = f"Error: {response.status_code} - {response.text}"
                        st.error(error_msg)
                        st.info("💡 **Troubleshooting Tips:**\n\n1. Verify your API key is correct\n2. Enable 'Generative Language API' in Google Cloud Console\n3. Check API quota and billing settings")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.info("💡 **Need Help?** Check the Documentation tab for setup instructions.")

with tab2:
    st.subheader("📊 Analytics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model", model_type)
    with col2:
        st.metric("Temperature", f"{temperature:.2f}")
    with col3:
        st.metric("Total Messages", len(st.session_state.get("messages", [])))
    
    if st.session_state.get("messages"):
        st.divider()
        st.write("### Conversation History")
        for i, msg in enumerate(st.session_state.messages, 1):
            st.write(f"{i}. **{msg['role'].title()}:** {msg['content'][:100]}...")

with tab3:
    st.markdown("""
    ## RAG Chatbot with Google Gemini AI
    
    ### Features:
    - **Real-time AI responses** using Google's Gemini API (100% FREE)
    - **Multiple models** to choose from
    - **Adjustable temperature** for response creativity
    - **Chat history** for context-aware conversations
    - **24/7 Availability**
    
    ### Models:
    - `gemini-1.5-flash`: Fast responses, free tier
    - `gemini-1.5-pro`: More detailed responses, free tier
    
    ### Setup Instructions:
    
    #### 1. Get API Key
    - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
    - Click "Create API Key"
    - Copy your key
    
    #### 2. Enable API
    - Go to [Google Cloud Console](https://console.cloud.google.com/)
    - Enable "Generative Language API"
    - Set up billing if required (free tier available)
    
    #### 3. Add to Streamlit
    - In Streamlit Cloud: Settings > Secrets
    - Add: `GOOGLE_API_KEY = "your-key-here"`
    
    ### Test Questions:
    - "What are your business hours?"
    - "How do I track my order?"
    - "What is your return policy?"
    - "How can I reset my password?"
    
    ### Need Help?
    - Check [GitHub Repository](https://github.com/Usha2025-git/rag-chatbot-ai-pm) for more info
    - Review PRD.md for product requirements
    - See METRIC_PLAN.md for analytics details
    """)

st.sidebar.markdown(f"**Status**: ✅ API Connected")
st.sidebar.markdown(f"**Messages**: {len(st.session_state.get('messages', []))}")
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()
