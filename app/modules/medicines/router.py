from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.medicines.schemas import (
    MedicineCreate,
    MedicineResponse,
    MedicineQuery,
    MedicineListResponse
)
from app.modules.medicines.service import (
    create_medicine,
    get_all_medicines,
    get_medicine_by_id,
    search_medicines,
    delete_medicine,
)

router = APIRouter(prefix="/medicines", tags=["Medicines"])

# Create a new medicine
@router.post("/", response_model=MedicineResponse)
def create_medicine(
    medicine: MedicineCreate,
    db: Session = Depends(get_db)
):
    return create_medicine(db, medicine)

# Get all medicines with pagination/filters
@router.get("/", response_model=MedicineListResponse)
def get_medicines(
    category: str = Query(None),
    pharmacy_id: int = Query(None),
    skip: int = Query(0),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    query = MedicineQuery(category=category, pharmacy_id=pharmacy_id, skip=skip, limit=limit)
    return get_all_medicines(db, query)

# Get single medicine by id (/id/{id})
@router.get("/id/{medicine_id}", response_model=MedicineResponse)
def get_medicine(
    medicine_id: int,
    db: Session = Depends(get_db)
):
    medicine = get_medicine_by_id(db, medicine_id)

    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    return medicine

# Search medicine by name
@router.get("/search", response_model=MedicineListResponse)
def search_medicine(
    name: str,
    db: Session = Depends(get_db)
):
    return search_medicines(db, name)


@router.delete("/{medicine_id}")
def delete_medicine_handler(
    medicine_id: int,
    db: Session = Depends(get_db)
):
    delete_medicine(db, medicine_id)
    return {"message": "Medicine deleted"} 


