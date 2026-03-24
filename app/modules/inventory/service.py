from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from .models import Inventory
from .schemas import InventoryCreate, InventoryUpdate, InventoryQuery
from sqlalchemy.orm import aliased
from app.modules.medicines.models import Medicine

def create_inventory(db: Session, inventory: InventoryCreate):

    db_inventory = Inventory(**inventory.model_dump())

    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)

    return db_inventory

def get_inventory_by_pharmacy(db: Session, pharmacy_id: int):

    return db.query(Inventory).filter(
        Inventory.pharmacy_id == pharmacy_id
    ).all()

def get_all(db: Session, query: InventoryQuery = None):
    if query is None:
        query = InventoryQuery()
    
    stmt = db.query(Inventory).join(Inventory.pharmacy).join(Inventory.medicine)
    
    if query.pharmacy_id:
        stmt = stmt.filter(Inventory.pharmacy_id == query.pharmacy_id)
    if query.medicine_id:
        stmt = stmt.filter(Inventory.medicine_id == query.medicine_id)
    if query.min_stock:
        stmt = stmt.filter(Inventory.stock_quantity <= query.min_stock)
    
    return stmt.offset(query.skip).limit(query.limit).all()

def get_by_id(db: Session, inventory_id: int):
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()

def get_by_medicine(db: Session, medicine_id: int):
    return db.query(Inventory).filter(
        Inventory.medicine_id == medicine_id
    ).all()

def search_inventory(db: Session, q: str, pharmacy_id: Optional[int] = None):
    medicine_alias = aliased(Medicine)
    stmt = db.query(Inventory).join(medicine_alias, Inventory.medicine_id == medicine_alias.id).join(Inventory.pharmacy)
    stmt = stmt.filter(medicine_alias.name.ilike(f"%{q}%"))
    if pharmacy_id:
        stmt = stmt.filter(Inventory.pharmacy_id == pharmacy_id)
    return stmt.all()

def update_inventory(db: Session, inventory_id: int, data: InventoryUpdate):

    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if not inventory:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(inventory, key, value)

    db.commit()
    db.refresh(inventory)

    return inventory

def delete_inventory(db: Session, inventory_id: int):

    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if not inventory:
        return None

    db.delete(inventory)
    db.commit()

    return inventory

