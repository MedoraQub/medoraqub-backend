from pydantic import BaseModel
from typing import Optional


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

    class Config:
        from_attributes = True