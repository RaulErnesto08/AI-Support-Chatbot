import json

from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def call_gpt_with_retries(client, messages, json_schema):
    """
    Calls the GPT API with retries on failure.
    """
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_schema", "json_schema": json_schema},
        max_tokens=1000,
        temperature=0.7,
    )

def generate_chatbot_response(user_message, api_key):
    """
    Generate a chatbot response using GPT.
    """
    client = OpenAI(api_key=api_key)

    try:
        json_schema = {
            "name": "chatbot_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "response": {"type": "string"}
                },
                "required": ["response"],
                "additionalProperties": False
            }
        }

        prompt = (
            f"You are an AI chatbot assistant. Respond helpfully and concisely to the user's message:\n"
            f"### User Message:\n"
            f"{user_message}\n\n"
            f"### Instructions:\n"
            f"1. Provide a clear and helpful response to the user's message.\n"
        )

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]

        response = call_gpt_with_retries(client, messages, json_schema)
        result = json.loads(response.choices[0].message.content)

        return result["response"]
    except Exception as e:
        print(f"Error generating chatbot response: {e}")
        return "I'm sorry, I encountered an error processing your request."
