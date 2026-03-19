from sqlalchemy.orm import Session
from .models import Medicine


#  Search medicines by name
def search_medicines(db: Session, name: str):

    medicines = (
        db.query(Medicine)
        .filter(Medicine.name.ilike(f"%{name}%"))
        .all()
    )

    return medicines


#  Get medicines by category
def get_medicines_by_category(db: Session, category: str):

    medicines = (
        db.query(Medicine)
        .filter(Medicine.category.ilike(category))
        .all()
    )

    return medicines