from fastapi import APIRouter

router = APIRouter()

@router.get("/message")
def get_message():
    return {"chatbot_message": "Hello!"}
