from app.utils.logging_config import setup_logger

logger = setup_logger()

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