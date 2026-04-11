from pydantic import BaseModel, Field, field_validator
from typing import Optional, Annotated, List, Generic, TypeVar
from decimal import Decimal

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    items: List[T]


class MedicineBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
    pharmacy_id: int = Field(..., gt=0)

    @field_validator("name", "description", "category")
    @classmethod
    def strip_strings(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Field cannot be empty or whitespace")
        return v

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]] = None

    @field_validator("name", "description", "category")
    @classmethod
    def strip_strings(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Field cannot be empty or whitespace")
        return v

class MedicineResponse(MedicineBase):
    id: int

    class Config:
        from_attributes = True

class MedicineQuery(BaseModel):
    category: Optional[str] = Field(None, min_length=1)
    pharmacy_id: Optional[int] = Field(None, gt=0)
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)

MedicineListResponse = PaginatedResponse[MedicineResponse]

