from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sdk.core.utils.logger import setup_logger

logger=setup_logger(__name__)

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )
