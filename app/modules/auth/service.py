from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.users.models import User
from app.core.security import verify_password, create_access_token, hash_password


def register_user(email: str, password: str, full_name: str, db: Session):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(password)

    # Create new user
    new_user = User(
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        role="user"  # default role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return token