from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.orders.service import create_order
from app.core.security import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/create")
def create_order_endpoint(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    order = create_order(db, current_user.id)

    return {
        "message": "Order created successfully",
        "order_id": order.id
    }