import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.healthcheck import router as health_router
from backend.api.image import router as image_router
from backend.api.items import router as items_router
from backend.config import get_settings

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI(
    title="Vanguard Vision API",
    description="API for reporting and managing found explosive items",
    docs_url="/docs" if settings.DEBUG else None,
)

# for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(image_router)
app.include_router(items_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# python -m backend.app
