#!/usr/bin/python3
import logging
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import Peon Modules
from modules.api_v1 import router as api_v1_router
from modules.servers import *
from modules.scheduler import *
from modules.shared import configure_logging

cors_allowed_headers = ["Content-Type", "api_key", "Authorization"]
cors_allowed_methods = ["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"]

# Configure logging first
configure_logging()
logging.info("[START]")

# Initialize FastAPI
app = FastAPI(
    title="PEON Orchestrator API",
    description="PEON orchestrator control plane API",
    version=os.environ.get("VERSION") or "1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=cors_allowed_methods,
    allow_headers=cors_allowed_headers,
)

app.include_router(api_v1_router, prefix="/api/v1")


@app.on_event("startup")
def startup() -> None:
    # Start the scheduler loop and prime server cache.
    scheduler_tick()
    servers_get_all()

# Start FastAPI listener
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=False)
    logging.debug("[END]")
