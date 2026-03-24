from sqlalchemy.orm import Session
from .models import Medicine
from .schemas import MedicineQuery

def create_medicine(db, medicine):
    db_medicine = Medicine(
        name=medicine.name,
        description=medicine.description,
        category=medicine.category,
        price=medicine.price,
        pharmacy_id=medicine.pharmacy_id
    )
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine

def get_all_medicines(db: Session, query: MedicineQuery = None):
    if query is None:
        query = MedicineQuery()
    
    stmt = db.query(Medicine)
    
    if query.category:
        stmt = stmt.filter(Medicine.category.ilike(f"%{query.category}%"))
    if query.pharmacy_id:
        stmt = stmt.filter(Medicine.pharmacy_id == query.pharmacy_id)
    
    return stmt.offset(query.skip).limit(query.limit).all()

def get_medicine_by_id(db: Session, medicine_id: int):
    return db.query(Medicine).filter(Medicine.id == medicine_id).first()

def search_medicines(db: Session, name: str):
    return db.query(Medicine).filter(
        Medicine.name.ilike(f"%{name}%")
    ).all()

def get_medicines_by_category(db: Session, category: str):
    return db.query(Medicine).filter(
        Medicine.category.ilike(f"%{category}%")
    ).all()

def delete_medicine(db: Session, medicine_id: int):
    medicine = get_medicine_by_id(db, medicine_id)
    if medicine:
        db.delete(medicine)
        db.commit()

