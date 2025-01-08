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
            response = fetch_user_input(user_message)

        # Validate the response and extract necessary fields
        if isinstance(response, dict):
            content = response.get("response", "No response provided.")
            action_result = response.get("action_result", None)

            st.markdown(content)

            st.session_state.messages.append({"role": "assistant", "content": content})

            if action_result:
                 st.toast(f"{action_result}", icon="✅")
        else:
            st.error("Unexpected response format from backend.")