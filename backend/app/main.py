from fastapi import FastAPI
from app.utils.logging_config import setup_logger
from app.routes.debug import router as debug_router
from app.routes.message import router as message_router
from app.routes.user_input import router as user_input_router
from app.utils.custom_error_handler import add_custom_error_handler

app = FastAPI()
logger = setup_logger()

app.include_router(message_router)
app.include_router(user_input_router)

add_custom_error_handler(app)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
