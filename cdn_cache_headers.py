from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class CDNCacheHeaders(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        resp = await call_next(request)
        if request.method == "GET" and resp.status_code == 200:
            # public for CDNs, brief micro-TTL, and fast revalidation
            resp.headers.setdefault("Cache-Control", "public, s-maxage=15, stale-while-revalidate=60")
            # helpful for some CDNs:
            resp.headers.setdefault("Surrogate-Control", "max-age=15, stale-while-revalidate=60")
        return resp