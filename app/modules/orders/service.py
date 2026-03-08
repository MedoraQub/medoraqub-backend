from sqlalchemy.orm import Session

from app.modules.cart.models import Cart
from app.modules.orders.models import Order, OrderItem
from app.modules.inventory.models import Inventory


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
    )

    db.add(order)
    db.flush()  # get order.id before commit

    # 3️⃣ Process each cart item
    for item in cart.items:

        inventory = db.query(Inventory).filter(
            Inventory.medicine_id == item.medicine_id
        ).first()

        if not inventory:
            raise Exception("Medicine not available")

        if inventory.quantity < item.quantity:
            raise Exception("Insufficient stock")

        # reduce inventory
        inventory.quantity -= item.quantity

        # calculate price
        item_price = inventory.price * item.quantity
        total_price += item_price

        order_item = OrderItem(
            order_id=order.id,
            medicine_id=item.medicine_id,
            quantity=item.quantity,
            price=inventory.price
        )

        db.add(order_item)

    # 4️⃣ Update total price
    order.total_price = total_price

    # 5️⃣ Clear cart items
    cart.items.clear()

    db.commit()
    db.refresh(order)

    return order