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
