from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.medicines.models import Medicine
from app.modules.medicines.schemas import MedicineCreate, MedicineResponse

router = APIRouter(prefix="/medicines", tags=["Medicines"])

# Create a new medicine
@router.post("/", response_model=MedicineResponse)
def create_medicine(
    medicine: MedicineCreate,
    db: Session = Depends(get_db)
):
    new_medicine = Medicine(**medicine.model_dump())

    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)

    return new_medicine

# Get all medicines
@router.get("/")
def get_medicines(db: Session = Depends(get_db)):

    medicines = db.query(Medicine).all()

    return medicines


# get single medicine by id
@router.get("/{medicine_id}")
def get_medicine(
    medicine_id: int,
    db: Session = Depends(get_db)
):

    medicine = db.query(Medicine).filter(
        Medicine.id == medicine_id
    ).first()

    if not medicine:
        raise Exception("Medicine not found")

    return medicine

# search medicine by name
@router.get("/search/{name}")
def search_medicine(
    name: str,
    db: Session = Depends(get_db)
):

    medicines = db.query(Medicine).filter(
        Medicine.name.ilike(f"%{name}%")
    ).all()

    return medicines