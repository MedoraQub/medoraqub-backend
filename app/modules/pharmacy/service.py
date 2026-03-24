from sqlalchemy.orm import Session
from sqlalchemy import func
from app.modules.pharmacy.models import Pharmacy
from app.modules.pharmacy.schemas import PharmacyCreate, PharmacyUpdate, PharmacyQuery
from app.modules.inventory.models import Inventory

def create_pharmacy(db: Session, pharmacy: PharmacyCreate):
    db_pharmacy = Pharmacy(**pharmacy.model_dump())
    db.add(db_pharmacy)
    db.commit()
    db.refresh(db_pharmacy)
    return db_pharmacy

def get_pharmacies(db: Session, query: PharmacyQuery = None):
    if query is None:
        query = PharmacyQuery()
    
    stmt = db.query(Pharmacy)
    
    if query.name:
        stmt = stmt.filter(Pharmacy.name.ilike(f"%{query.name}%"))
    
    stmt = stmt.offset(query.skip).limit(query.limit)
    
    pharmacies = stmt.all()
    
    # Add avg_inventory_stock
    for p in pharmacies:
        avg_stock = db.query(func.avg(Inventory.stock_quantity)).filter(Inventory.pharmacy_id == p.id).scalar()
        p.avg_inventory_stock = avg_stock if avg_stock else 0
    
    return pharmacies

def get_pharmacy_by_id(db: Session, pharmacy_id: int):
    return db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()

def get_low_inventory_pharmacies(db: Session, min_avg_stock: float = 10, skip: int = 0, limit: int = 100):
    stmt = db.query(Pharmacy)
    stmt = stmt.join(Inventory).group_by(Pharmacy.id).having(func.avg(Inventory.stock_quantity) <= min_avg_stock)
    return stmt.offset(skip).limit(limit).all()

def update_pharmacy(db: Session, pharmacy_id: int, pharmacy: PharmacyUpdate):
    db_pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()

    if not db_pharmacy:
        return None

    update_data = pharmacy.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_pharmacy, key, value)

    db.commit()
    db.refresh(db_pharmacy)

    return db_pharmacy

def delete_pharmacy(db: Session, pharmacy_id: int):
    db_pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()

    if not db_pharmacy:
        return None

    db.delete(db_pharmacy)
    db.commit()

    return db_pharmacy

