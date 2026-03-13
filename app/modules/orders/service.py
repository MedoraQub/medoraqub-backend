from sqlalchemy.orm import Session

from app.modules.cart.models import Cart
from app.modules.orders.models import Order, OrderItem
from app.modules.inventory.models import Inventory
from app.modules.medicines.models import Medicine


def create_order(db: Session, user_id: int):

    # 1️⃣ Get user cart
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart or not cart.items:
        raise Exception("Cart is empty")

    total_price = 0

    # 2️⃣ Create Order
    order = Order(
        user_id=user_id,
        total_price=0
        status = "pending"
    )

    db.add(order)
    db.flush()  # get order.id

    # 3️⃣ Process cart items
    for item in cart.items:

        inventory = db.query(Inventory).filter(
            Inventory.medicine_id == item.medicine_id
        ).first()

        if not inventory:
            raise Exception("Medicine not available")

        if inventory.stock_quantity < item.quantity:
            raise Exception("Insufficient stock")

        # get medicine for price
        medicine = db.query(Medicine).filter(
            Medicine.id == item.medicine_id
        ).first()

        # reduce stock
        inventory.stock_quantity -= item.quantity

        item_price = medicine.price * item.quantity
        total_price += item_price

        order_item = OrderItem(
            order_id=order.id,
            medicine_id=item.medicine_id,
            quantity=item.quantity,
            price=medicine.price
        )

        db.add(order_item)

    # 4️⃣ Update total
    order.total_price = total_price

    # 5️⃣ Clear cart
    cart.items.clear()

    db.commit()
    db.refresh(order)

    return order

def get_user_orders(db: Session, user_id: int):

    orders = db.query(Order).filter(Order.user_id == user_id).all()

    return orders


def get_order_by_id(db: Session, user_id: int, order_id: int):

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()

    if not order:
        raise Exception("Order not found")

    return order


def update_order_status(db: Session, order_id: int, status: str):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise Exception("Order not found")

    order.status = status

    db.commit()
    db.refresh(order)

    return order