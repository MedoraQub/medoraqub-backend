from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class OrderItem(Base, TimestampMixin):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    medicine_id: Mapped[int] = mapped_column(
        ForeignKey("medicines.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    price_at_purchase: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    medicine_name_snapshot: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # =========================
    # Relationships
    # =========================

    order = relationship("Order", back_populates="items")

    medicine = relationship(
        "Medicine",
        back_populates="order_items"
    )