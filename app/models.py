"""Data models for the watering-api."""

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Rule(Base):
    """Watering rule for a plant type.

    Attributes:
        plant_type: Plant type (e.g. ``vegetable``); primary key.
        interval_days: Days between one watering and the next.
        rain_threshold_mm: Expected rain, in mm, above which watering is
            postponed.
    """

    __tablename__ = "rules"

    plant_type: Mapped[str] = mapped_column(String(50), primary_key=True)
    interval_days: Mapped[int] = mapped_column(Integer)
    rain_threshold_mm: Mapped[float] = mapped_column(Float)
