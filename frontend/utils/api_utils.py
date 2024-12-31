import logging
import requests

BACKEND_URL = "http://127.0.0.1:8000"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("frontend_logger")

def fetch_message():
    try:
        response = requests.get(f"{BACKEND_URL}/message", timeout=5)
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
            timeout=5,
        )
        
        response.raise_for_status()
        chatbot_response = response.json().get("response", "No response received.")
        logger.info(f"Received chatbot response from backend: {chatbot_response}")
        
        return chatbot_response
    except requests.exceptions.RequestException as e:
        logger.error(f"API error: {e}")
        return f"API error: {e}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"An unexpected error occurred: {e}"
