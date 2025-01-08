import os
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

def call_openai_formatter(langchain_response: str) -> dict:
    """Call OpenAI API to format LangChain response into valid JSON."""
    client = OpenAI(
            api_key = os.getenv("OPENAI_API_KEY")
        )
    
    json_schema = {
        "name": "json_formatter",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "response_type": {"type": "string", "enum": ["intent", "text"]},
                "intent": {"type": ["string", "null"]},
                "content": {"type": "string"},
                "order_details": {
                    "type": ["object", "null"],
                    "properties": {
                        "order_number": {"type": "string"},
                        "size": {"type": "string"},
                        "toppings": {"type": "array", "items": {"type": "string"}},
                        "name": {"type": "string"},
                        "status": {"type": "string"},
                    },
                    "required": ["order_number", "size", "toppings", "name", "status"],
                    "additionalProperties": False
                },
            },
            "required": ["response_type", "intent", "content", "order_details"],
            "additionalProperties": False
        }
    }

    prompt = (
        f"Transform the following response into a valid JSON format based on the schema provided:\n\n"
        f"### Rules:\n"
        f"1. Always classify the response into one of the following 'response_type' categories:\n"
        f"   - 'intent': For task-related actions such as the order is created or the order is cancelled.\n"
        f"   - 'text': For general responses not associated with specific tasks.\n"
        f"2. If 'response_type' is 'intent', ensure the 'intent' field is set to the appropriate task name ('create_order', 'cancel_order').\n"
        f"3. If 'response_type' is 'text', set 'intent' to null.\n"
        f"4. For 'intent' responses, include 'order_details' with the following fields: 'order_number', 'size', 'toppings', 'name', and 'status'.\n"
        f"5. Once you detected the order is beign completed or canceled, mark the response_type as intent accordingly.\n"
        f"6. For 'text' responses, set 'order_details' to null.\n"
        f"7. Ensure the response adheres strictly to the schema.\n\n"
        f"### Response:\n{langchain_response}\n\n"
        f"### Output:\n"
    )
    
    messages = [
            {"role": "system", "content": "Format the following into valid JSON based on the provided schema."},
            {"role": "user", "content": prompt},
    ]
    
    response = call_gpt_with_retries(client, messages, json_schema)
    
    result = json.loads(response.choices[0].message.content)
    
    print(f"OpenAI Formatter Result: {result}")
    
    return result