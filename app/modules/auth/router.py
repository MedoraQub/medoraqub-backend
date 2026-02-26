from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.auth.schema import RegisterRequest, LoginRequest, TokenResponse
from app.modules.auth.service import register_user
from app.core.security import (
    verify_password,
    create_access_token,
    get_current_user
)
from app.modules.users.models import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================
# Register
# =========================

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    user = register_user(
        email=data.email,
        password=data.password,
        full_name=data.full_name,
        db=db
    )

    return {
        "message": "User registered successfully",
        "user_id": user.id
    }


# =========================
# Login
# =========================

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================
# Get Current User
# =========================

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):

    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active
    }