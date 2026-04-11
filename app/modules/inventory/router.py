from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from .schemas import InventoryCreate, InventoryUpdate, InventoryResponse, InventoryListResponse, InventoryQuery
from app.modules.inventory import service

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

@router.post("/", response_model=InventoryResponse, status_code=201)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):
    return service.create_inventory(db, inventory)

@router.get("/", response_model=InventoryListResponse)
def list_inventory(
    pharmacy_id: Optional[int] = Query(None),
    medicine_id: Optional[int] = Query(None),
    min_stock: Optional[int] = Query(0, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = InventoryQuery(
        pharmacy_id=pharmacy_id,
        medicine_id=medicine_id,
        min_stock=min_stock,
        skip=skip,
        limit=limit
    )
    result = service.get_all(db, query)
    if result['total'] == 0:
        raise HTTPException(status_code=404, detail="No inventory found")
    return result



@router.get("/search", response_model=InventoryListResponse)
def search_inventory(
    name: str = Query(..., min_length=1),
    pharmacy_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return service.search_inventory(db, name, pharmacy_id, skip, limit)

@router.get("/low-stock", response_model=InventoryListResponse)
def get_low_stock_inventory(
    pharmacy_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    min_stock: int = Query(10, ge=0),
    db: Session = Depends(get_db)
):
    query = InventoryQuery(
        pharmacy_id=pharmacy_id,
        min_stock=min_stock,
        skip=skip,
        limit=limit
    )
    result = service.get_all(db, query)
    if result['total'] == 0:
        raise HTTPException(status_code=404, detail="No low stock inventory found")
    return result

@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory_by_id(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    inventory = service.get_by_id(db, inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: int,
    data: InventoryUpdate,
    db: Session = Depends(get_db)
):

    inventory = service.update_inventory(db, inventory_id, data)

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    return inventory

@router.delete("/{inventory_id}", status_code=204)
def delete_inventory(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    success = service.delete_inventory(db, inventory_id)
    if not success:
        raise HTTPException(status_code=404,detail="Inventory not found")
    return {"message": "Inventory is deleted"}