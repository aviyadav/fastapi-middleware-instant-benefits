import time, asyncio
from functools import lru_cache
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response

class MicroCacheMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, ttl=10):
        super().__init__(app)
        self.ttl = ttl
        self._locks = {}

    @lru_cache(maxsize=4096)
    def _cache_key(self, method, url, auth):
        return f"{method}:{url}:{auth}"

    async def dispatch(self, request: Request, call_next):
        if request.method != "GET":
            return await call_next(request)

        key = self._cache_key("GET", str(request.url), request.headers.get("authorization", ""))
        lock = self._locks.setdefault(key, asyncio.Lock())

        async with lock:  # prevents stampedes
            cached: tuple | None = request.app.state.__dict__.get(key)  # (expiry, bytes, headers, status, media_type)
            now = time.time()
            if cached and cached[0] > now:
                expiry, body, headers, status, mt = cached
                r = Response(content=body, status_code=status, media_type=mt)
                for k, v in headers.items():
                    if k.lower() != "content-length":
                        r.headers[k] = v
                r.headers["X-Microcache"] = "HIT"
                return r

            resp = await call_next(request)
            body = b"".join([b async for b in resp.body_iterator])
            if resp.status_code == 200:
                request.app.state.__dict__[key] = (now + self.ttl, body, dict(resp.headers), resp.status_code, resp.media_type)
            r = Response(content=body, status_code=resp.status_code, media_type=resp.media_type)
            r.headers.update(dict(resp.headers))
            r.headers["X-Microcache"] = "MISS"
            return r