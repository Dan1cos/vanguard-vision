import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from backend.db.schemas import HealthCheckResponse

router = APIRouter(
    prefix="/api",
    tags=["Health"],
)

logger = logging.getLogger("healthcheck")


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health check endpoint",
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service is unhealthy"},
    },
)
async def health_check():
    try:
        result = {
            "status": "healthy",
        }
        return JSONResponse(result, status_code=200)
    except Exception as e:
        logger.exception("Health check failed")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")
