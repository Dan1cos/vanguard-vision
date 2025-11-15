import uuid

import sqlalchemy as sa
from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class ItemType(Base):
    __tablename__ = "item_type"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        nullable=False,
    )
    title = Column(String, nullable=False)
    explosion_radius = Column(Float, nullable=False)


class FoundItem(Base):
    __tablename__ = "found_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        nullable=False,
    )
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    type_id = Column(UUID(as_uuid=True), ForeignKey("item_type.id"), nullable=False)
    created_at = Column(sa.DateTime(), nullable=False, server_default=sa.func.now())
