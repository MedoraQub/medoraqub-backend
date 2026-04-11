from pydantic import BaseModel, Field
from typing import Optional, Annotated, List, Generic, TypeVar
from decimal import Decimal

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    items: List[T]

class InventoryBase(BaseModel):
    pharmacy_id: int = Field(..., gt=0)
    medicine_id: int = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    stock_quantity: Optional[int] = Field(None, ge=0)
    price: Optional[Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]] = None

class InventoryResponse(InventoryBase):
    id: int
    medicine_name: Optional[str] = None
    pharmacy_name: Optional[str] = None

    class Config:
        from_attributes = True

class InventoryQuery(BaseModel):
    pharmacy_id: Optional[int] = Field(None, gt=0)
    medicine_id: Optional[int] = Field(None, gt=0)
    min_stock: Optional[int] = Field(0, ge=0)
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)

InventoryListResponse = PaginatedResponse[InventoryResponse]

