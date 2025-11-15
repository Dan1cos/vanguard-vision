import uuid

from sqlalchemy.orm import Session

from . import schemas, tables


# ---- ItemType ----
def create_item_type(db: Session, obj: schemas.ItemTypeCreate):
    db_obj = tables.ItemType(**obj.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_item_types(db: Session):
    return db.query(tables.ItemType).all()


def get_item_type_by_title(db: Session, title: str):
    return db.query(tables.ItemType).filter(tables.ItemType.title == title).first()


def get_item_type_by_id(db: Session, type_id: uuid.UUID):
    return db.query(tables.ItemType).filter(tables.ItemType.id == type_id).first()


# ---- FoundItem ----
def create_found_item(db: Session, obj: schemas.FoundItemCreate):
    db_obj = tables.FoundItem(**obj.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_found_items(db: Session):
    return db.query(tables.FoundItem).all()


def get_found_item(db: Session, item_id: uuid.UUID):
    return db.query(tables.FoundItem).filter(tables.FoundItem.id == item_id).first()
