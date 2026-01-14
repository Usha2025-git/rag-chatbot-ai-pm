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

st.sidebar.header("⚙️ Settings")
model_type = st.sidebar.selectbox("Select Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)

tab1, tab2, tab3 = st.tabs(["Chat", "Analytics", "Documentation"])

with tab1:
    st.subheader("💬 Chat Interface")
    user_query = st.text_input("Your Question:")
    
    if st.button("🔍 Submit"):
        if user_query:
            with st.spinner("Processing your query..."):
                try:
                    # Call Google Gemini API
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_type}:generateContent?key={GOOGLE_API_KEY}"
                    headers = {
                        "Content-Type": "application/json"
                    }
                    data = {
                        "contents": [{
                            "parts": [{
                                "text": f"You are a helpful AI assistant for customer support. Answer this question: {user_query}"
                            }]
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
    ## RAG Chatbot with Google Gemini AI
    
    ### Features:
    - **Real-time AI responses** using Google's Gemini API (100% FREE)
    - **Multiple models** to choose from
    - **Adjustable temperature** for response creativity
    - **24/7 Availability**
    
    ### Models:
    - `gemini-1.5-flash`: Fast responses, free tier
    - `gemini-1.5-pro`: More detailed responses, free tier
    """)

st.sidebar.markdown("**Status**: ✅ API Connected")
