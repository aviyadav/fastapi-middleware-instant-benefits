import hashlib
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response

def _etag(data: bytes) -> str:
    return hashlib.blake2s(data, digest_size=8).hexdigest()

class ETagMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        candidate = request.headers.get("if-none-match")
        resp = await call_next(request)

        if resp.status_code == 200 and resp.headers.get("cache-control", "").find("no-store") == -1:
            body = [b async for b in resp.body_iterator]
            blob = b"".join(body)
            tag = _etag(blob)
            if candidate == tag:
                return Response(status_code=304, headers={"ETag": tag})
            r = Response(content=blob, status_code=resp.status_code, media_type=resp.media_type)
            r.headers.update(dict(resp.headers))
            r.headers["ETag"] = tag
            return r
        return resp