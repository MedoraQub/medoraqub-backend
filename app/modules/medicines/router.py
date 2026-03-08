from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.medicines.models import Medicine
from app.modules.medicines.schemas import MedicineCreate, MedicineResponse

router = APIRouter(prefix="/medicines", tags=["Medicines"])


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