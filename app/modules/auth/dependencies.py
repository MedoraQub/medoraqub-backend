from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.users.models import User


def get_current_user(db: Session = Depends(get_db)) -> User:
    """
    Temporary dependency until JWT auth is implemented.
    """

    user = db.query(User).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    return user