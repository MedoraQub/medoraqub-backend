from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db

from app.modules.pharmacy.schemas import (
    PharmacyCreate,
    PharmacyUpdate,
    PharmacyResponse
)

# Import CRUD functions
from app.modules.pharmacy.crud import (
    create_pharmacy,
    get_pharmacies,
    get_pharmacy_by_id,
    update_pharmacy,
    delete_pharmacy
)

# Define the router for pharmacy-related endpoints
router = APIRouter(
    prefix="/pharmacies",
    tags=["Pharmacies"]
)

# Endpoint to create a new pharmacy
@router.post("/", response_model=PharmacyResponse)
def create_new_pharmacy(
    pharmacy: PharmacyCreate,
    db: Session = Depends(get_db)
):
    return create_pharmacy(db, pharmacy)


# Endpoint to list all pharmacies
@router.get("/", response_model=List[PharmacyResponse])
def list_all_pharmacies(db: Session = Depends(get_db)):
    return get_pharmacies(db)


# Endpoint to get a single pharmacy by ID
@router.get("/{pharmacy_id}", response_model=PharmacyResponse)
def get_single_pharmacy(
    pharmacy_id: int,
    db: Session = Depends(get_db)
):
    pharmacy = get_pharmacy_by_id(db, pharmacy_id)

    if not pharmacy:
        raise HTTPException(
            status_code=404,
            detail="Pharmacy not found"
        )

    return pharmacy


# Endpoint to update an existing pharmacy
@router.put("/{pharmacy_id}", response_model=PharmacyResponse)
def update_existing_pharmacy(
    pharmacy_id: int,
    pharmacy: PharmacyUpdate,
    db: Session = Depends(get_db)
):
    updated = update_pharmacy(db, pharmacy_id, pharmacy)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Pharmacy not found"
        )

    return updated


# Endpoint to delete a pharmacy
@router.delete("/{pharmacy_id}")
def delete_existing_pharmacy(
    pharmacy_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_pharmacy(db, pharmacy_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Pharmacy not found"
        )

    return {"message": "Pharmacy deleted successfully"}
