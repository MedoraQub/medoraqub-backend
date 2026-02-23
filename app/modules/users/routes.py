from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.modules.users import models, schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ✅ Create User
@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        full_name=user.name,
        email=user.email,
        hashed_password="temp123"  # temporary for now
)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ✅ Get All Users
@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users