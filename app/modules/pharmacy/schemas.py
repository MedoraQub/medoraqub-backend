import re

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Annotated, List, Generic, TypeVar
from decimal import Decimal

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    items: List[T]

class PharmacyBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=10, max_length=255)
    phone: Optional[str] = Field(None)

    @field_validator("name", "address")
    @classmethod
    def strip_strings(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Field cannot be empty or whitespace")
        return v
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return v
        if not re.match(r'^\+?[1-9]\d{1,14}$', v):
            raise ValueError("Invalid phone number format")
        return v

class PharmacyCreate(PharmacyBase):
    owner_id: int

class PharmacyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    address: Optional[str] = Field(None, min_length=10, max_length=255)
    phone: Optional[str] = Field(None)

    @field_validator("name", "address")
    @classmethod
    def strip_strings(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Field cannot be empty or whitespace")
        return v
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return v
        if not re.match(r'^\+?[1-9]\d{1,14}$', v):
            raise ValueError("Invalid phone number format")
        return v

class PharmacyResponse(PharmacyBase):
    id: int
    owner_id: int
    avg_inventory_stock: Annotated[Optional[Decimal], Field(None, ge=0)] = None

    class Config:
        from_attributes = True

class PharmacyQuery(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)

PharmacyListResponse = PaginatedResponse[PharmacyResponse]

