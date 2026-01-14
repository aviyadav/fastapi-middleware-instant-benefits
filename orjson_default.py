from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import ORJSONResponse
from fastapi import Request

class ORJSONDefaultMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        resp = await call_next(request)
        if getattr(resp, "media_type", None) == "application/json" and not isinstance(resp, ORJSONResponse):
            # Re-wrap while preserving status and headers
            body = [section async for section in resp.body_iterator]
            merged = b"".join(body)
            new = ORJSONResponse(content=merged if merged else None,
                                 status_code=resp.status_code)
            for k, v in resp.headers.items():
                if k.lower() != "content-length":
                    new.headers[k] = v
            return new
        return resp