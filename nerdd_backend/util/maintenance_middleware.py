import logging

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)


class MaintenanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Exclude specific paths from maintenance interception (e.g., health checks)
        if request.url.path not in ("/health",):
            logger.info(
                "Blocking request %s %s due to active maintenance mode",
                request.method,
                request.url.path,
            )
            return JSONResponse(
                status_code=503,
                content={"detail": "Server is under maintenance.", "code": "under_maintenance"},
            )
        return await call_next(request)
