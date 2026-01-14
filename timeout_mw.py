import asyncio
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response

class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, default_timeout=1.5):
        super().__init__(app)
        self.default_timeout = default_timeout

    async def dispatch(self, request: Request, call_next):
        timeout = float(request.headers.get("x-timeout", self.default_timeout))
        try:
            return await asyncio.wait_for(call_next(request), timeout=timeout)
        except asyncio.TimeoutError:
            return Response("Deadline exceeded", status_code=524, media_type="text/plain")