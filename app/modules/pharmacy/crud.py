from sqlalchemy.orm import Session
from app.modules.pharmacy.models import Pharmacy
from app.modules.pharmacy.schemas import PharmacyCreate, PharmacyUpdate


def create_pharmacy(db: Session, pharmacy: PharmacyCreate):
    db_pharmacy = Pharmacy(**pharmacy.dict())
    db.add(db_pharmacy)
    db.commit()
    db.refresh(db_pharmacy)
    return db_pharmacy


def get_pharmacies(db: Session):
    return db.query(Pharmacy).all()


def get_pharmacy_by_id(db: Session, pharmacy_id: int):
    return db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()


def update_pharmacy(db: Session, pharmacy_id: int, pharmacy: PharmacyUpdate):
    db_pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()

    if not db_pharmacy:
        return None

    for key, value in pharmacy.dict(exclude_unset=True).items():
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