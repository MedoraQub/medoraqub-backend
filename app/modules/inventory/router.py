from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from . import service, schemas

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.post("/", response_model=schemas.InventoryResponse)
def create_inventory(
    inventory: schemas.InventoryCreate,
    db: Session = Depends(get_db)
):
    return service.create_inventory(db, inventory)


@router.get("/pharmacy/{pharmacy_id}")
def get_inventory_by_pharmacy(
    pharmacy_id: int,
    db: Session = Depends(get_db)
):
    return service.get_inventory_by_pharmacy(db, pharmacy_id)


@router.patch("/{inventory_id}", response_model=schemas.InventoryResponse)
def update_inventory(
    inventory_id: int,
    data: schemas.InventoryUpdate,
    db: Session = Depends(get_db)
):

    inventory = service.update_inventory(db, inventory_id, data)

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    return inventory


@router.delete("/{inventory_id}")
def delete_inventory(
    inventory_id: int,
    db: Session = Depends(get_db)
):

    inventory = service.delete_inventory(db, inventory_id)

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    return {"message": "Inventory deleted"}

