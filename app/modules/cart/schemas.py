from pydantic import BaseModel
from typing import List


class AddCartItem(BaseModel):
    medicine_id: int
    quantity: int


class UpdateCartItem(BaseModel):
    medicine_id: int
    quantity: int


class CartItemResponse(BaseModel):
    medicine_id: int
    quantity: int

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse]

    class Config:
        from_attributes = True