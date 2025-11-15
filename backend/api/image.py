import io
import os

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError

from backend import service

router = APIRouter(
    prefix="/api",
    tags=["Upload Image"],
)


@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    """Accepts an uploaded image, saves it to a temporary file, and
    forwards it to the prediction service

    Returns a JSON response with the path where the file was saved and
    prediction result when service.predict returns something meaningful
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    validate_file_size_type(file)

    try:
        content = await file.read()
        try:
            img = Image.open(io.BytesIO(content)).convert("RGB")
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
        return JSONResponse({"top_conf": float(top_conf), "top_name": str(top_name)})
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
