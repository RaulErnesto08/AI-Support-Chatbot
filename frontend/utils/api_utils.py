import os
import logging
import requests

from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("frontend_logger")

def fetch_message():
    try:
        response = requests.get(f"{BACKEND_URL}/message", timeout=10000)
        response.raise_for_status()
        return response.json().get("chatbot_message", "No message received.")
    except requests.exceptions.RequestException as e:
        return f"API error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def fetch_user_input(user_message):
    """
    Sends user input to the backend and retrieves the chatbot's response.
    """
    try:
        logger.info(f"Sending user input to backend: {user_message}")
        response = requests.post(
            f"{BACKEND_URL}/process-input",
            json={"message": user_message},
            timeout=10000,
        )
        
        response.raise_for_status()
        chatbot_response = response.json()
        logger.info(f"Received chatbot response from backend: {chatbot_response}")
        
        return chatbot_response
    except requests.exceptions.RequestException as e:
        error_message = f"API error: {e.response.text if e.response else str(e)}"
        logger.error(error_message)
        return {"error": error_message}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": f"An unexpected error occurred: {e}"}

def process_audio_file(audio_file):
    """Send audio file to backend and process it."""
    response = requests.post(
        f"{BACKEND_URL}/process-audio",
        files={"file": ("audio.wav", audio_file, "audio/wav")}
    )
    response.raise_for_status()
    return response.json()