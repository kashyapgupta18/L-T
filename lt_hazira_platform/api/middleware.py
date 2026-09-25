"""Request timing and logging middleware for FastAPI."""
import time
from starlette.middleware.base import BaseHTTPMiddleware
from lt_hazira_platform.core.logging_config import setup_logger

logger = setup_logger("api_middleware")

class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = round((time.time() - start_time) * 1000, 2)
        response.headers["X-Process-Time-Ms"] = str(process_time)
        logger.info(f"{request.method} {request.url.path} completed in {process_time}ms (status {response.status_code})")
        return response
