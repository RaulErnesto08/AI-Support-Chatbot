from fastapi import Request
from fastapi.responses import JSONResponse

def add_custom_error_handler(app):
    @app.exception_handler(Exception)
    async def custom_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": "An unexpected error occurred."},
        )
