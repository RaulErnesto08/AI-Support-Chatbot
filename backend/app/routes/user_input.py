from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.utils.logging_config import setup_logger
from app.utils.langchain_utils import setup_langchain
# from app.utils.openai_utils import generate_chatbot_response

router = APIRouter()
logger = setup_logger()
chatbot_chain = setup_langchain()

chat_history = []

class UserInput(BaseModel):
    user_message: str

@router.post("/process-input")
async def process_input(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    response = chatbot_chain({
        "question": user_message
    })
    
    return {"response": response["answer"]}