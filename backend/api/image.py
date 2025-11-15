import io
import logging
import os
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from backend import service
from backend.config import get_settings
from backend.db import crud
from backend.db.database import get_db
from backend.db.schemas import DetectionResult, FoundItemCreate
from backend.utils.gps import (extract_gps_coordinates,
                               generate_random_coordinates)

settings = get_settings()
logger = logging.getLogger("image_detection")


router = APIRouter(
    prefix="/api",
    tags=["Image Detection"],
)


@router.post(
    "/image",
    response_model=DetectionResult,
    summary="Detect objects in uploaded image",
    response_description="Detection results with confidence scores",
    responses={
        200: {
            "description": "Successful detection",
            "content": {
                "application/json": {
                    "example": {
                        "top_conf": 0.95,
                        "top_name": "aircraft-bombs",
                        "lat": 37.7749,
                        "lon": -122.4194,
                        "explosion_radius": 100.0,
                    }
                }
            },
        },
        400: {"description": "Invalid image file or unsupported format"},
        413: {"description": "File too large (max 2MB)"},
        415: {"description": "Unsupported media type"},
        500: {"description": "Prediction service error"},
    },
)
async def upload_image(
    file: UploadFile = File(
        ...,
        description="Image file to analyze (PNG, JPEG, WebP, HEIC/HEIF). Max size: 2MB",
    ),
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    db: Session = Depends(get_db),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    validate_file_size_type(file)

    try:
        content = await file.read()
        try:
            img_original = Image.open(io.BytesIO(content))
            if lat is None or lon is None:
                gps_coords = extract_gps_coordinates(img_original)
                if gps_coords:
                    lat, lon = gps_coords
                    logger.info(
                        f"Extracted GPS coordinates from image: lat={lat}, lon={lon}"
                    )
                else:
                    lat, lon = generate_random_coordinates()
                    logger.info(
                        f"No GPS data found. Using random coordinates: lat={lat:.4f}, lon={lon:.4f}"
                    )

            img = img_original.convert("RGB")
        except UnidentifiedImageError:
            raise HTTPException(
                status_code=400, detail="Uploaded file is not a valid image"
            )

        try:
            results = service.predict(img)
        except Exception as e:
            return JSONResponse(
                {"error": "prediction_failed", "detail": str(e)}, status_code=500
            )

        top_conf = results[0].probs.top1conf
        top_name = results[0].names[results[0].probs.top1]
        item_type = None

        if float(top_conf) >= settings.MIN_PREDICTION_CONFIDENCE:
            try:
                item_type = crud.get_item_type_by_title(db, top_name)

                if item_type is not None:
                    found_item_data = FoundItemCreate(
                        lat=lat, lon=lon, type_id=item_type.id
                    )
                    saved_item = crud.create_found_item(db, found_item_data)
                    logger.info(
                        f"Saved found item to database: {saved_item.id} at ({lat}, {lon})"
                    )
                elif not item_type:
                    logger.warning(
                        f"Item type '{top_name}' not found in database. Skipping save."
                    )
            except Exception as e:
                logger.warning(
                    f"Warning: Failed to save prediction to database: {str(e)}"
                )

        response = {
            "top_conf": float(top_conf),
            "top_name": str(top_name),
            "lat": lat,
            "lon": lon,
            "explosion_radius": item_type.explosion_radius if item_type else None,
        }
        return JSONResponse(response, status_code=200)
    finally:
        await file.close()


def validate_file_size_type(upload_file: UploadFile, max_bytes: int = 2 * 1024 * 1024):
    """Validate uploaded file-ish object for allowed mime/type and size

    This function will read/seek the underlying file object but will restore
    the cursor to the start so the file can be read again by the caller
    """
    accepted_mimes = {
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/webp",
        "image/heic",
        "image/heif",
    }

    if upload_file.content_type not in accepted_mimes:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported media type: {upload_file.content_type}",
        )

    fobj = upload_file.file

    try:
        fobj.seek(0, os.SEEK_END)
        size = fobj.tell()
    except Exception:
        size = 0
        chunks = []
        fobj.seek(0)
        while True:
            chunk = fobj.read(64 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
            if size > max_bytes:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Too large",
                )
        fobj.seek(0)

    if size > max_bytes:
        fobj.seek(0)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too large"
        )

    try:
        fobj.seek(0)
        with Image.open(fobj) as img:
            img.verify()
            fmt = (img.format or "").lower()
            if fmt not in {"jpeg", "png", "gif", "webp", "heic", "heif"}:
                pass
    except UnidentifiedImageError:
        fobj.seek(0)
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Uploaded file is not a valid image",
        )
    except Exception:
        fobj.seek(0)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file"
        )

    fobj.seek(0)
