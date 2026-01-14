from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
import brotli

class BrotliLargeTextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, min_size=64_000):
        super().__init__(app)
        self.min_size = min_size

    async def dispatch(self, request: Request, call_next):
        resp = await call_next(request)
        if "br" in request.headers.get("accept-encoding", "") and resp.media_type in ("application/json", "text/plain", "text/html"):
            body = b"".join([b async for b in resp.body_iterator])
            if len(body) >= self.min_size:
                compressed = brotli.compress(body)
                r = Response(content=compressed, status_code=resp.status_code, media_type=resp.media_type)
                r.headers.update(dict(resp.headers))
                r.headers["Content-Encoding"] = "br"
                r.headers.pop("Content-Length", None)
                return r
            return Response(content=body, status_code=resp.status_code, media_type=resp.media_type, headers=dict(resp.headers))
        return resp

# Use both:
# app.add_middleware(GZipMiddleware, minimum_size=1000)
# app.add_middleware(BrotliLargeTextMiddleware, min_size=64_000)