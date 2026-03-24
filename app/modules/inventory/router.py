from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from .service import *
from .schemas import InventoryCreate, InventoryUpdate, InventoryResponse, InventoryListResponse, InventoryQuery
from app.modules.inventory import service

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

@router.post("/", response_model=InventoryResponse)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):
    return service.create_inventory(db, inventory)

@router.get("/", response_model=InventoryListResponse)
def get_all_inventory(
    pharmacy_id: Optional[int] = Query(None),
    medicine_id: Optional[int] = Query(None),
    min_stock: Optional[int] = Query(0),
    skip: int = Query(0),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    query = InventoryQuery(
        pharmacy_id=pharmacy_id,
        medicine_id=medicine_id,
        min_stock=min_stock,
        skip=skip,
        limit=limit
    )
    return service.get_all(db, query)

@router.get("/id/{inventory_id}", response_model=InventoryResponse)
def get_inventory_by_id(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    inventory = service.get_by_id(db, inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory


@router.get("/low-stock", response_model=InventoryListResponse)
def get_low_stock_inventory(
    pharmacy_id: Optional[int] = Query(None),
    min_stock: int = Query(10),
    skip: int = Query(0),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    query = InventoryQuery(
        pharmacy_id=pharmacy_id,
        min_stock=min_stock,
        skip=skip,
        limit=limit
    )
    return service.get_all(db, query)

@router.get("/search", response_model=InventoryListResponse)
def search_inventory(
    Search: str,
    pharmacy_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    return service.search_inventory(db, Search, pharmacy_id)

@router.patch("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: int,
    data: InventoryUpdate,
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
