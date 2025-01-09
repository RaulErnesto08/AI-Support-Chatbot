import streamlit as st
from audiorecorder import audiorecorder
from utils.api_utils import process_audio_file

st.set_page_config(page_title="AI Support Chatbot", layout="wide")
st.title("AI Support Chatbot - Voice")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "sentiment" not in st.session_state:
    st.session_state.sentiment = "🙂"

# Display sentiment emoji
emoji_placeholder = st.empty()
emoji_placeholder.markdown(
    f"<div style='text-align: center; font-size: 24px;'>{st.session_state.sentiment}</div>",
    unsafe_allow_html=True,
)

# Audio recorder
audio = audiorecorder("Click to record", "Click to stop recording")

if len(audio) > 0:
    audio.export("audio.wav", format="wav")
    st.audio("audio.wav", format="audio/wav", autoplay=True)

    with open("audio.wav", "rb") as audio_file:
        with st.spinner("Processing audio..."):
            result = process_audio_file(audio_file)

        user_input = result.get("user_input", "")
        answer = result.get("answer", "")
        audio_reply = result.get("audio_reply", "")
        sentiment = result.get("sentiment", "neutral")
        action_result = result.get("action_result", None)

        # Update sentiment emoji
        if sentiment == "negative":
            st.session_state.sentiment = "😟"
        elif sentiment == "positive":
            st.session_state.sentiment = "😄"
        else:
            st.session_state.sentiment = "🙂"

        emoji_placeholder.markdown(
            f"<div style='text-align: center; font-size: 24px;'>{st.session_state.sentiment}</div>",
            unsafe_allow_html=True,
        )

        # Update chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Display chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Play audio reply
        st.audio(audio_reply, format="audio/wav", autoplay=True)

        # Show toast notification for action results
        if action_result:
            st.toast(f"{action_result}", icon="✅")
