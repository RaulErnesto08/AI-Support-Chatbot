from transformers import pipeline
from app.utils.logging_config import setup_logger

logger = setup_logger()
sentiment_pipeline = pipeline("sentiment-analysis")

def perform_mocked_action(intent: str, response_data: dict) -> str:
    """Perform a mocked action based on the detected intent."""
    
    actions = {
        "create_order": f"Order {response_data['order_details']['order_number']} created successfully for {response_data['order_details']['name']}.",
        "cancel_order": f"Order {response_data['order_details']['order_number']} has been canceled.",
    }
    
    action_message = actions.get(intent, "No valid action performed.")
    logger.info(f"Mocked Action: {action_message}")
    return action_message

def perform_escalation_action(response_data: dict) -> str:
    """
    Perform a mocked escalation action when the intent is 'escalate_to_human'.
    """
    
    logger.warning(f"Escalating issue to human agent: {response_data}")
    return "Your query has been escalated to a human agent. Please wait for further assistance."

def analyze_sentiment_transformers(text: str) -> str:
    """
    Analyze sentiment of the given text using Hugging Face Transformers.
    Returns: 'positive', 'neutral', or 'negative'.
    """
    result = sentiment_pipeline(text)[0]
    label = result["label"].lower()
    print(f"Sentiment Analysis Result: {result}")
    print(f"Sentiment Label: {label}")
    if label in ["positive", "neutral", "negative"]:
        return label
    return "neutral"