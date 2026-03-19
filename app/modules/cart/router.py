from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.orders import service
from app.modules.orders.service import create_order
from app.core.security import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


# =========================
# CREATE ORDER
# =========================
@router.post("/create")
def create_order_endpoint(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        order = create_order(db, current_user.id)

        return {
            "message": "Order created successfully",
            "order_id": order.id
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================
# GET USER ORDERS
# =========================
@router.get("/my-orders")
def get_my_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return service.get_user_orders(db, user.id)


# =========================
# GET SINGLE ORDER
# =========================
@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return service.get_order_by_id(db, user.id, order_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# =========================
# UPDATE ORDER STATUS
# =========================
@router.patch("/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    try:
        return service.update_order_status(db, order_id, status)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# =========================
# CANCEL ORDER
# =========================
@router.delete("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return service.cancel_order(db, user.id, order_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    