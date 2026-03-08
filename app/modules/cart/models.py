from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Cart(Base, TimestampMixin):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    # Relationships
    user = relationship("User", back_populates="cart")

    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )


class CartItem(Base, TimestampMixin):
    __tablename__ = "cart_items"

    __table_args__ = (
        UniqueConstraint("cart_id", "medicine_id", name="unique_cart_medicine"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    medicine_id: Mapped[int] = mapped_column(
        ForeignKey("medicines.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )

    # Relationships
    cart = relationship("Cart", back_populates="items")
    medicine = relationship("Medicine")