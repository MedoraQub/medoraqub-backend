from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemBase(BaseModel):
    medicine_id: int
    quantity: int
    price: float


class OrderItemResponse(OrderItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    total_price: float
    status: str


class OrderResponse(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True