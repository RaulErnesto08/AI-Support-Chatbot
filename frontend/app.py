import streamlit as st

from utils.api_utils import fetch_user_input

st.set_page_config(page_title="AI Support Chatbot", layout="wide")
st.title("AI Support Chatbot")

user_message = st.text_input("Enter your message:")

if st.button("Send"):
    if user_message.strip():
        with st.spinner("Processing your message..."):
            response = fetch_user_input(user_message)
        
        if response:
            st.success(f"Chatbot: {response}")
        else:
            st.error("No response received. Please try again.")
    else:
        st.error("Please enter a valid message.")
