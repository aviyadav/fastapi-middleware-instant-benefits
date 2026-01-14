from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from orjson_default import ORJSONDefaultMiddleware
from etag_mw import ETagMiddleware
from microcache_mw import MicroCacheMiddleware
from singleflight_mw import SingleFlightMiddleware
from compression_mw import GZipMiddleware, BrotliLargeTextMiddleware
from background_mw import BackgroundFinalizeMiddleware
from timeout_mw import TimeoutMiddleware
from cdn_cache_headers import CDNCacheHeaders

app = FastAPI(default_response_class=ORJSONResponse)

app.add_middleware(ORJSONDefaultMiddleware)
app.add_middleware(ETagMiddleware)
app.add_middleware(SingleFlightMiddleware)
app.add_middleware(MicroCacheMiddleware, ttl=10)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(BrotliLargeTextMiddleware, min_size=64_000)
app.add_middleware(BackgroundFinalizeMiddleware)
app.add_middleware(TimeoutMiddleware, default_timeout=1.5)
app.add_middleware(CDNCacheHeaders)

@app.get("/health")
async def health():
    return {"ok": True}