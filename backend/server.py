from contextlib import asynccontextmanager
import time
import error_handling
from fastapi.exceptions import RequestValidationError
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import uvicorn
import structlog
import asyncio

log: structlog.stdlib.BoundLogger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await setup_elevenlabs_websocket()
    log.info("Starting up")
    yield

    log.info("Shutting down")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/status")
async def status():
    return {"status": "hunk-dory"}


@app.exception_handler(error_handling.CanonicalException)
async def canonical_exception_handler(
    request: Request, exc: error_handling.CanonicalException
):
    log.info(f"Caught exception: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": str(exc),
            "details": exc.details,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    log.error("Validation error", errs=exc.errors(), body=await request.body())
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
