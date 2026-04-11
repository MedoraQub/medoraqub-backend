from typing import Optional
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from .models import Inventory
from .schemas import InventoryCreate, InventoryUpdate, InventoryQuery
from sqlalchemy.orm import aliased
from app.modules.medicines.models import Medicine

def create_inventory(db: Session, inventory: InventoryCreate):
    try:
        db_inventory = Inventory(**inventory.model_dump())
        db.add(db_inventory)
        db.commit()
        db.refresh(db_inventory)
        return db_inventory
    except SQLAlchemyError:
        db.rollback()
        raise

def get_inventory_by_pharmacy(db: Session, pharmacy_id: int):

    return db.query(Inventory).filter(
        Inventory.pharmacy_id == pharmacy_id
    ).all()

def get_all(db: Session, query: InventoryQuery = None):
    if query is None:
        query = InventoryQuery()
    
    stmt = db.query(Inventory).join(Inventory.pharmacy).join(Inventory.medicine).options(joinedload(Inventory.pharmacy), joinedload(Inventory.medicine))
    
    if query.pharmacy_id:
        stmt = stmt.filter(Inventory.pharmacy_id == query.pharmacy_id)
    if query.medicine_id:
        stmt = stmt.filter(Inventory.medicine_id == query.medicine_id)
    if query.min_stock:
        stmt = stmt.filter(Inventory.stock_quantity <= query.min_stock)
    
    total = stmt.count()
    items = stmt.offset(query.skip).limit(query.limit).all()
    return {'total': total, 'items': items}

def get_by_id(db: Session, inventory_id: int):
    return db.query(Inventory).filter_by(id=inventory_id).first()

def get_by_medicine(db: Session, medicine_id: int):
    return db.query(Inventory).filter(
        Inventory.medicine_id == medicine_id
    ).all()

def search_inventory(db: Session, q: str, pharmacy_id: Optional[int] = None, skip: int = 0, limit: int = 10):
    medicine_alias = aliased(Medicine)
    stmt = db.query(Inventory).join(medicine_alias, Inventory.medicine_id == medicine_alias.id).join(Inventory.pharmacy).options(joinedload(Inventory.pharmacy), joinedload(Inventory.medicine))
    stmt = stmt.filter(medicine_alias.name.ilike(f"%{q}%"))
    if pharmacy_id:
        stmt = stmt.filter(Inventory.pharmacy_id == pharmacy_id)
    total = stmt.count()
    items = stmt.offset(skip).limit(limit).all()
    return {'total': total, 'items': items}

def update_inventory(db: Session, inventory_id: int, data: InventoryUpdate):

    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if not inventory:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(inventory, key, value)

    try:
        db.commit()
        db.refresh(inventory)
        return inventory
    except SQLAlchemyError:
        db.rollback()
        return None

def delete_inventory(db: Session, inventory_id: int):
    try:
        inventory = db.query(Inventory).filter_by(id=inventory_id).first()
        if not inventory:
            return False
        db.delete(inventory)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        return False
