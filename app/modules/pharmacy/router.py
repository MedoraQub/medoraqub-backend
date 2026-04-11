from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.modules.pharmacy.schemas import (
    PharmacyCreate,
    PharmacyUpdate,
    PharmacyResponse,
    PharmacyQuery,
    PharmacyListResponse
)

# Import CRUD functions
from app.modules.pharmacy.services import (
    create_pharmacy,
    get_pharmacies,
    get_pharmacy_by_id,
    get_low_inventory_pharmacies,
    update_pharmacy,
    delete_pharmacy
)

# Define the router for pharmacy-related endpoints
router = APIRouter(
    prefix="/pharmacies",
    tags=["Pharmacies"]
)

# Endpoint to create a new pharmacy
@router.post("/", response_model=PharmacyResponse, status_code=201)
def create_new_pharmacy(
    pharmacy: PharmacyCreate,
    db: Session = Depends(get_db)
):
    return create_pharmacy(db, pharmacy)

# Endpoint to list all pharmacies with filters/pagination
@router.get("/", response_model=PharmacyListResponse)
def list_all_pharmacies(
    name: str = Query(None, min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = PharmacyQuery(name=name, skip=skip, limit=limit)
    result = get_pharmacies(db, query)
    if result["total"] == 0:
        raise HTTPException(status_code=404, detail="No pharmacy found")
    return result

# Endpoint to get pharmacies with low inventory
@router.get("/low-inventory", response_model=PharmacyListResponse)
def list_low_inventory_pharmacies(
    min_avg_stock: float = Query(10, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    result = get_low_inventory_pharmacies(db, min_avg_stock, skip, limit)
    if result["total"] == 0:
        raise HTTPException(status_code=404, detail="No pharmacy found")
    return result

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
@router.patch("/{pharmacy_id}", response_model=PharmacyResponse)
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
    success = delete_pharmacy(db, pharmacy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pharmacy not found")
    return {"message": "Pharmacy is deleted"}
