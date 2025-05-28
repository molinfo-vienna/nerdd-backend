import logging

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)


class LogRequestsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        logger.info(f"Incoming request: {request.method} {request.url.path}")

        client_host = request.client.host if request.client else "N/A"
        logger.info(f"* Client IP (request.client.host): {client_host}")

        x_headers = {
            key: value for key, value in request.headers.items() if key.lower().startswith("x-")
        }

        for key, value in x_headers.items():
            logger.info(f"* {key}: {value}")

        response = await call_next(request)

        logger.info(f"* Response: Status {response.status_code}")

        for key, value in response.headers.items():
            logger.info(f"* Response Header {key}: {value}")

        return response
