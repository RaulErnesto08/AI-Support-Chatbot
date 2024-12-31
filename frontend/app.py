import streamlit as st

from utils.api_utils import fetch_user_input

st.set_page_config(page_title="AI Support Chatbot", layout="wide")
st.title("AI Support Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_message := st.chat_input("Enter your message:"):
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Please wait..."):
            assistant_response = fetch_user_input(user_message)
        st.markdown(assistant_response)
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
