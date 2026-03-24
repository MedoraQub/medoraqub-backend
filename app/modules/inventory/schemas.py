from pydantic import BaseModel
from typing import Optional, List

class InventoryBase(BaseModel):
    pharmacy_id: int
    medicine_id: int
    stock_quantity: int
    price: float

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    stock_quantity: Optional[int]
    price: Optional[float]

class InventoryResponse(InventoryBase):
    id: int
    medicine_name: Optional[str] = None
    pharmacy_name: Optional[str] = None

    class Config:
        from_attributes = True

class InventoryQuery(BaseModel):
    pharmacy_id: Optional[int] = None
    medicine_id: Optional[int] = None
    min_stock: Optional[int] = 0
    skip: int = 0
    limit: int = 100

InventoryListResponse = List[InventoryResponse]

