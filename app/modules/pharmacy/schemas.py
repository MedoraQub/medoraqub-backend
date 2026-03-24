from pydantic import BaseModel
from typing import Optional, List

class PharmacyBase(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None

class PharmacyCreate(PharmacyBase):
    owner_id: int

class PharmacyUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class PharmacyResponse(PharmacyBase):
    id: int
    owner_id: int
    avg_inventory_stock: Optional[float] = None

    class Config:
        from_attributes = True

class PharmacyQuery(BaseModel):
    name: Optional[str] = None
    skip: int = 0
    limit: int = 100

PharmacyListResponse = List[PharmacyResponse]

