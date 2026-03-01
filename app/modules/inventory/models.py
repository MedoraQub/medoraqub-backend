from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Inventory(Base, TimestampMixin):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    medicine_id: Mapped[int] = mapped_column(
        ForeignKey("medicines.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # ensures one inventory per medicine
        index=True
    )

    stock_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    # =========================
    # Relationships
    # =========================

    medicine = relationship("Medicine", back_populates="inventory")