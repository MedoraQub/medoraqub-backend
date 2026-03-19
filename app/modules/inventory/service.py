from sqlalchemy.orm import Session
from .models import Inventory
from .schemas import InventoryCreate, InventoryUpdate


def create_inventory(db: Session, inventory: InventoryCreate):

    db_inventory = Inventory(**inventory.model_dump())

    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)

    return db_inventory


def get_inventory_by_pharmacy(db: Session, pharmacy_id: int):

    return db.query(Inventory).filter(
        Inventory.pharmacy_id == pharmacy_id
    ).all()


def update_inventory(db: Session, inventory_id: int, data: InventoryUpdate):

    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if not inventory:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(inventory, key, value)

    db.commit()
    db.refresh(inventory)

    return inventory


def delete_inventory(db: Session, inventory_id: int):

    inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()

    if not inventory:
        return None

    db.delete(inventory)
    db.commit()

    return inventory