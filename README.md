# FastAPI Middleware Instant

A collection of reusable FastAPI middleware components for common API patterns.

## Features

| Middleware | Description |
|------------|-------------|
| `ORJSONDefaultMiddleware` | Converts JSON responses to use faster ORJSON serialization |
| `ETagMiddleware` | Adds ETag headers and handles `304 Not Modified` responses |
| `SingleFlightMiddleware` | Deduplicates concurrent identical requests |
| `MicroCacheMiddleware` | Short-lived in-memory response caching |
| `GZipMiddleware` | Compresses responses using gzip |
| `BrotliLargeTextMiddleware` | Brotli compression for large text responses |
| `BackgroundFinalizeMiddleware` | Handles background task finalization |
| `TimeoutMiddleware` | Request timeout handling |
| `CDNCacheHeaders` | Adds CDN-friendly cache headers |

## Requirements

- Python >= 3.14
- FastAPI >= 0.128.0

## Installation

```bash
uv sync
```

## Usage

```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from orjson_default import ORJSONDefaultMiddleware
from etag_mw import ETagMiddleware

app = FastAPI(default_response_class=ORJSONResponse)

app.add_middleware(ORJSONDefaultMiddleware)
app.add_middleware(ETagMiddleware)

@app.get("/health")
async def health():
    return {"ok": True}
```

## Running

```bash
uvicorn main:app --reload
```

## License

MIT