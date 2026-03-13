from pydantic import BaseModel
from typing import Optional


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

    class Config:
        from_attributes = True

        