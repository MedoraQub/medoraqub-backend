from sqlalchemy import String, Numeric, ForeignKey, Text
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Medicine(Base, TimestampMixin):
    __tablename__ = "medicines"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    pharmacy_id: Mapped[int] = mapped_column(
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # =========================
    # Relationships
    # =========================

    pharmacy = relationship("Pharmacy", back_populates="medicines")
    inventory = relationship(
        "Inventory",
        back_populates="medicine"
    )
    order_items = relationship("OrderItem", back_populates="medicine")