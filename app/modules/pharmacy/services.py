from itertools import count

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Result
from app.modules.pharmacy.models import Pharmacy
from app.modules.pharmacy.schemas import PharmacyCreate, PharmacyUpdate, PharmacyQuery, PharmacyResponse
from decimal import Decimal
from app.modules.inventory.models import Inventory

def create_pharmacy(db: Session, pharmacy: PharmacyCreate):
    try:
        db_pharmacy = Pharmacy(**pharmacy.model_dump())
        db.add(db_pharmacy)
        db.commit()
        db.refresh(db_pharmacy)
        return db_pharmacy
    except SQLAlchemyError:
        db.rollback()
        raise

def get_pharmacies(db: Session, query: PharmacyQuery = None):
    if query is None:
        query = PharmacyQuery()

    stmt = select(
        Pharmacy.id,
        Pharmacy.name,
        Pharmacy.address,
        Pharmacy.phone,
        Pharmacy.owner_id,
        func.coalesce(func.avg(Inventory.stock_quantity), 0).label("avg_stock")
    ).select_from(
        Pharmacy.__table__.outerjoin(Inventory.__table__, Pharmacy.id == Inventory.pharmacy_id)
    ).group_by(
        Pharmacy.id, Pharmacy.name, Pharmacy.address, Pharmacy.phone, Pharmacy.owner_id
    )

    if query.name:
        stmt = stmt.where(Pharmacy.name.ilike(f"%{query.name}%"))


    # Count total
    count_stmt = select(func.count()).select_from(
        stmt.subquery()
    )
    total = db.scalar(count_stmt)

    results = db.execute(
        stmt.offset(query.skip).limit(query.limit)
    ).all()

    items = []
    for row in results:
        row_dict = dict(row._mapping)
        avg_stock = row_dict.pop("avg_stock")
        row_dict["avg_inventory_stock"] = Decimal(avg_stock) if avg_stock is not None else Decimal("0")
        items.append(PharmacyResponse.model_validate(row_dict))

    return {"total": total or 0, "items": items}

def get_pharmacy_by_id(db: Session, pharmacy_id: int):
    return db.query(Pharmacy).filter_by(id=pharmacy_id).first()

def get_low_inventory_pharmacies(db: Session, min_avg_stock: float = 10, skip: int = 0, limit: int = 10):
    stmt = select(
        Pharmacy.id,
        Pharmacy.name,
        Pharmacy.address,
        Pharmacy.phone,
        Pharmacy.owner_id,
        func.coalesce(func.avg(Inventory.stock_quantity), 0).label("avg_stock")
    ).select_from(
        Pharmacy.__table__.outerjoin(Inventory.__table__, Pharmacy.id == Inventory.pharmacy_id)
    ).group_by(
        Pharmacy.id, Pharmacy.name, Pharmacy.address, Pharmacy.phone, Pharmacy.owner_id
    ).having(
        func.coalesce(func.avg(Inventory.stock_quantity), 0) <= min_avg_stock
    )


    # Count total
    count_stmt = select(func.count()).select_from(
        stmt.subquery()
    )
    total = db.scalar(count_stmt)

    results = db.execute(
        stmt.offset(skip).limit(limit)
    ).all()

    items = []
    for row in results:
        row_dict = dict(row._mapping)
        avg_stock = row_dict.pop("avg_stock")
        row_dict["avg_inventory_stock"] = Decimal(avg_stock) if avg_stock is not None else Decimal("0")
        items.append(PharmacyResponse.model_validate(row_dict))

    return {"total": total or 0, "items": items}

def update_pharmacy(db: Session, pharmacy_id: int, pharmacy: PharmacyUpdate):
    db_pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()

    if not db_pharmacy:
        return None

    update_data = pharmacy.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_pharmacy, key, value)

    try:
        db.commit()
        db.refresh(db_pharmacy)
        return db_pharmacy
    except SQLAlchemyError:
        db.rollback()
        return None

def delete_pharmacy(db: Session, pharmacy_id: int):
    try:
        db_pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()
        if not db_pharmacy:
            return False
        db.delete(db_pharmacy)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        return False

