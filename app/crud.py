from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate, ItemUpdate


def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


def get_item_by_name(db: Session, name: str):
    return db.query(Item).filter(Item.name == name).first()


def create_item(db: Session, item: ItemCreate):
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: ItemUpdate):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db_item.name = item.name
        db_item.description = item.description
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
