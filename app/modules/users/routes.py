from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.modules.users import models, schemas
from app.core.security import get_current_user
from app.modules.users.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



# Get All Users
@router.get("/", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = db.query(models.User).all()
    return users