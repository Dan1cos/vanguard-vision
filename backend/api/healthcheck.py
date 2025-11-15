import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/api",
    tags=["Health"],
)

logger = logging.getLogger("healthcheck")


@router.get("/health")
async def health_check():
    try:
        result = {
            "status": "healthy",
        }
        return JSONResponse(result, status_code=200)
    except Exception as e:
        logger.exception("Health check failed")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")
