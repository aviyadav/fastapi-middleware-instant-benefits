from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class BackgroundFinalizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        resp = await call_next(request)

        def _finalize():
            # lightweight side-effects
            # e.g., queue analytics, fire-and-forget webhook, warm cache
            pass

        if not getattr(resp, "background", None):
            resp.background = BackgroundTask(_finalize)
        return resp