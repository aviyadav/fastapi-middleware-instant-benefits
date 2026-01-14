from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
import asyncio, hashlib

class SingleFlightMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._inflight: dict[str, asyncio.Future] = {}

    def _key(self, request: Request) -> str:
        raw = f"{request.method}:{request.url}"
        return hashlib.md5(raw.encode(), usedforsecurity=False).hexdigest()

    async def dispatch(self, request: Request, call_next):
        if request.method != "GET":
            return await call_next(request)

        k = self._key(request)
        if k in self._inflight:
            return await self._inflight[k]

        fut: asyncio.Future = asyncio.get_event_loop().create_future()
        self._inflight[k] = fut
        try:
            resp = await call_next(request)
            body = b"".join([b async for b in resp.body_iterator])
            r = Response(content=body, status_code=resp.status_code, media_type=resp.media_type)
            r.headers.update(dict(resp.headers))
            fut.set_result(r)
            return r
        finally:
            self._inflight.pop(k, None)