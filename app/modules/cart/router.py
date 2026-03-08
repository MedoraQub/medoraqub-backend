from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.auth.dependencies import get_current_user

from . import service
from .schemas import AddCartItem, UpdateCartItem

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/add-item")
def add_item(
    data: AddCartItem,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return service.add_item_to_cart(db, user.id, data.medicine_id, data.quantity)


@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return service.get_cart(db, user.id)


@router.patch("/update-quantity")
def update_quantity(
    data: UpdateCartItem,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return service.update_quantity(db, user.id, data.medicine_id, data.quantity)


@router.delete("/remove-item/{medicine_id}")
def remove_item(
    medicine_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return service.remove_item(db, user.id, medicine_id)


@router.delete("/clear")
def clear_cart(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return service.clear_cart(db, user.id)