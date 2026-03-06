from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    role: Mapped[str] = mapped_column(String(50), default="user", index=True)

    # =========================
    # Relationships
    # =========================

    pharmacies = relationship("Pharmacy", back_populates="owner")
    orders = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    cart = relationship("Cart", back_populates="user", uselist=False)
    addresses = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete-orphan"
    )