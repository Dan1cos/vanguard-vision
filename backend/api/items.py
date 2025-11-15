import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db import crud, schemas
from backend.db.database import get_db

router = APIRouter(
    prefix="/api/items",
    tags=["Items"],
)


# ---- ItemType Endpoints ----
@router.get(
    "/types",
    response_model=List[schemas.ItemType],
    summary="Get all item types",
    response_description="List of all explosive item types",
    responses={
        200: {
            "description": "Successful retrieval of item types",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "title": "aircraft-bombs",
                            "explosion_radius": 100.0,
                        }
                    ]
                }
            },
        },
        500: {"description": "Database error"},
    },
)
async def get_all_item_types(db: Session = Depends(get_db)):
    """
    Retrieve all item types from the database.

    Returns a list of all explosive item types with their explosion radius.
    """
    try:
        item_types = crud.get_item_types(db)
        return item_types
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve item types: {str(e)}",
        )


# ---- FoundItem Endpoints ----
@router.get(
    "/found",
    response_model=List[schemas.FoundItem],
    summary="Get all found items",
    response_description="List of all found explosive items",
    responses={
        200: {
            "description": "Successful retrieval of found items",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "lat": 50.4501,
                            "lon": 30.5234,
                            "type_id": "123e4567-e89b-12d3-a456-426614174001",
                            "created_at": "2024-01-15T10:30:00",
                        }
                    ]
                }
            },
        },
        500: {"description": "Database error"},
    },
)
async def get_all_found_items(db: Session = Depends(get_db)):
    """
    Retrieve all found items from the database.

    Returns a list of all reported explosive items with their locations.
    """
    try:
        found_items = crud.get_found_items(db)
        return found_items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve found items: {str(e)}",
        )


@router.get(
    "/found/{item_id}",
    response_model=schemas.FoundItem,
    summary="Get found item by ID",
    response_description="Found item details",
    responses={
        200: {
            "description": "Successful retrieval",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "lat": 50.4501,
                        "lon": 30.5234,
                        "type_id": "123e4567-e89b-12d3-a456-426614174001",
                        "created_at": "2024-01-15T10:30:00",
                    }
                }
            },
        },
        404: {"description": "Found item not found"},
        500: {"description": "Database error"},
    },
)
async def get_found_item_by_id(item_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Retrieve a specific found item by its ID.

    - **item_id**: The UUID of the found item to retrieve
    """
    try:
        found_item = crud.get_found_item(db, item_id)
        if not found_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Found item with ID '{item_id}' not found",
            )
        return found_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve found item: {str(e)}",
        )
