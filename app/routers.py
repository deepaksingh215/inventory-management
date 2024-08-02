import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
import crud, schemas, cache
import logs
# Configure the logger

router = APIRouter()
logger = logs.logger

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating item with name: {item.name}")
    db_item = crud.get_item_by_name(db, name=item.name)
    if db_item:
        logger.warning(f"Item with name {item.name} already exists")
        raise HTTPException(status_code=400, detail="Item already exists")

    created_item = crud.create_item(db=db, item=item)
    logger.info(f"Item created with ID: {created_item.id}")
    return created_item


@router.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    logger.info(f"Reading item with ID: {item_id}")
    cached_item = await cache.get_item_from_cache(item_id)
    if cached_item:
        logger.info(f"Item with ID {item_id} found in cache")
        return cached_item

    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        logger.error(f"Item with ID {item_id} not found")
        raise HTTPException(status_code=404, detail="Item not found")

    item = schemas.Item.from_orm(db_item)
    await cache.set_item_to_cache(item_id, item)
    logger.info(f"Item with ID {item_id} cached")
    return db_item


@router.put("/items/{item_id}", response_model=schemas.Item)
async def update_item(
    item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)
):
    logger.info(f"Updating item with ID: {item_id}")
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        logger.error(f"Item with ID {item_id} not found")
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item = crud.update_item(db=db, item_id=item_id, item=item)
    logger.info(f"Item with ID {item_id} updated")
    return updated_item


@router.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting item with ID: {item_id}")
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        logger.error(f"Item with ID {item_id} not found")
        raise HTTPException(status_code=404, detail="Item not found")

    crud.delete_item(db=db, item_id=item_id)
    logger.info(f"Item with ID {item_id} deleted")
    return {"message": "Item deleted successfully"}
