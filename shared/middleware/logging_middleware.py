import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        
        # Log request details
        logger.info(f"Request: {request.method} {request.url.path} - Headers: {request.headers}")
        
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = f'{process_time:.2f}ms'
        
        # Log response details
        logger.info(
            f"Response: {request.method} {request.url.path} - Status: {response.status_code} - Process Time: {formatted_process_time}"
        )
        response.headers["X-Process-Time"] = formatted_process_time
        return response

# To use this middleware in a FastAPI app:
# from shared.middleware.logging_middleware import RequestLoggingMiddleware
# app.add_middleware(RequestLoggingMiddleware) 