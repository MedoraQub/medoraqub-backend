from sqlalchemy.orm import Session

from .models import Cart, CartItem
from app.modules.inventory.models import Inventory
from app.modules.medicines.models import Medicine


def get_or_create_cart(db: Session, user_id: int):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart


def add_item_to_cart(db: Session, user_id: int, medicine_id: int, quantity: int):

    cart = get_or_create_cart(db, user_id)

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.medicine_id == medicine_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            medicine_id=medicine_id,
            quantity=quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return cart


def get_cart(db: Session, user_id: int):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    return cart


def update_quantity(db: Session, user_id: int, medicine_id: int, quantity: int):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.medicine_id == medicine_id
    ).first()

    cart_item.quantity = quantity

    db.commit()
    db.refresh(cart_item)

    return cart


def remove_item(db: Session, user_id: int, medicine_id: int):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.medicine_id == medicine_id
    ).first()

    db.delete(cart_item)

    db.commit()

    return {"message": "Item removed"}


def clear_cart(db: Session, user_id: int):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

    db.commit()

    return {"message": "Cart cleared"}