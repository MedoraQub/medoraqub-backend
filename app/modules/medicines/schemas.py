from pydantic import BaseModel
from typing import Optional, List

class MedicineBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    pharmacy_id: int

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None

class MedicineResponse(MedicineBase):
    id: int

    class Config:
        from_attributes = True

class MedicineQuery(BaseModel):
    category: Optional[str] = None
    pharmacy_id: Optional[int] = None
    skip: int = 0
    limit: int = 100

MedicineListResponse = List[MedicineResponse]

