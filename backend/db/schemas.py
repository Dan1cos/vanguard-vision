import uuid

from pydantic import BaseModel


class ItemTypeBase(BaseModel):
    title: str
    explosion_radius: float


class ItemTypeCreate(ItemTypeBase):
    pass


class ItemType(ItemTypeBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class FoundItemBase(BaseModel):
    lat: float
    lon: float
    type_id: uuid.UUID
    created_at: str


class FoundItemCreate(FoundItemBase):
    pass


class FoundItem(FoundItemBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


# API Response schemas for documentation
class DetectionResult(BaseModel):
    """Response model for image detection endpoint"""
    top_conf: float
    top_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "top_conf": 0.95,
                "top_name": "aircraft-bombs"
            }
        }


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy"
            }
        }
