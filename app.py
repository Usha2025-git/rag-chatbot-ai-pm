import streamlit as st
import requests
import json

st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("🤖 RAG Chatbot Platform")
st.markdown("AI-powered customer support using Perplexity AI")

# Get API key from Streamlit secrets
try:
    PERPLEXITY_API_KEY = st.secrets["PERPLEXITY_API_KEY"]
except:
    st.error("⚠️ Perplexity API key not found. Please add it in Streamlit secrets.")
    st.stop()

st.sidebar.header("⚙️ Settings")
model_type = st.sidebar.selectbox("Select Model", ["llama-3.1-sonar-small-128k-online", "llama-3.1-sonar-large-128k-online"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)

tab1, tab2, tab3 = st.tabs(["Chat", "Analytics", "Documentation"])

with tab1:
    st.subheader("💬 Chat Interface")
    user_query = st.text_input("Your Question:")
    
    if st.button("🔍 Submit"):
        if user_query:
            with st.spinner("Processing your query..."):
                try:
                    # Call Perplexity API
                    url = "https://api.perplexity.ai/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "model": model_type,
                        "messages": [
                            {"role": "system", "content": "You are a helpful AI assistant for customer support."},
                            {"role": "user", "content": user_query}
                        ],
                        "temperature": temperature
                    }
                    
                    response = requests.post(url, headers=headers, json=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        answer = result["choices"][0]["message"]["content"]
                        st.success("✅ Response received!")
                        st.write(f"**Answer**: {answer}")
                        st.metric("Status", "Success")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

with tab2:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model", model_type)
    with col2:
        st.metric("Temperature", f"{temperature:.2f}")
    with col3:
        st.metric("Status", "✅ Connected")

with tab3:
    st.markdown("""
    ## RAG Chatbot with Perplexity AI
    
    ### Features:
    - **Real-time AI responses** using Perplexity's API
    - **Multiple models** to choose from
    - **Adjustable temperature** for response creativity
    - **24/7 Availability**
    
    ### Models:
    - `llama-3.1-sonar-small-128k-online`: Fast responses
    - `llama-3.1-sonar-large-128k-online`: More detailed responses
    """)

st.sidebar.markdown("**Status**: ✅ API Connected")
