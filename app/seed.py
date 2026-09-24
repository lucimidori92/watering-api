"""Default rules created on the watering-api's first run."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Rule

DEFAULT_RULES: tuple[tuple[str, int, float], ...] = (
    ("vegetable", 1, 5.0),
    ("herb", 2, 5.0),
    ("fruit_tree", 3, 10.0),
    ("succulent", 7, 2.0),
)


def create_default_rules(session: Session) -> None:
    """Creates the default rules if the rules table is empty.

    Args:
        session: SQLAlchemy session used to persist the rules.
    """
    if session.scalar(select(Rule).limit(1)) is not None:
        return
    session.add_all(
        Rule(plant_type=plant_type, interval_days=interval, rain_threshold_mm=rain)
        for plant_type, interval, rain in DEFAULT_RULES
    )
    session.commit()
