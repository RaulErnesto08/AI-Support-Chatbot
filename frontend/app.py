import streamlit as st

from utils.api_utils import fetch_user_input

st.title("AI Support Chatbot")

user_message = st.text_input("Enter your message:")

if st.button("Send"):
    if user_message.strip():
        response = fetch_user_input(user_message)
        st.success(f"Response: {response}")
    else:
        st.error("Please enter a message.")
