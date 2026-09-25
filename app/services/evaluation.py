"""Pure watering decision logic, isolated from the database and HTTP layers."""

from datetime import date, timedelta

from app.models import Rule
from app.schemas import EvaluationResult, PlantEvaluation


def evaluate_plant(
    plant: PlantEvaluation, rule: Rule | None, today: date
) -> EvaluationResult:
    """Decides whether to water, postpone, wait, or flag a missing rule.

    Args:
        plant: The plant being evaluated, with its last watering date and
            the rain expected for it.
        rule: The watering rule for the plant's type, or ``None`` if no
            rule is registered for that type.
        today: The current date, used to compute elapsed and next-watering
            days.

    Returns:
        The watering decision, its reason, and (when applicable) the date
        of the next watering.
    """
    if rule is None:
        return EvaluationResult(
            plant_id=plant.plant_id,
            decision="no_rule",
            reason=f"No watering rule registered for plant type '{plant.plant_type}'.",
            next_watering=None,
        )

    if plant.last_watered_at is None:
        return EvaluationResult(
            plant_id=plant.plant_id,
            decision="water",
            reason="This plant has never been watered.",
            next_watering=today,
        )

    days_since_watering = (today - plant.last_watered_at).days
    next_scheduled = plant.last_watered_at + timedelta(days=rule.interval_days)

    if days_since_watering < rule.interval_days:
        return EvaluationResult(
            plant_id=plant.plant_id,
            decision="wait",
            reason=(
                f"Watered {days_since_watering} day(s) ago; the rule waits "
                f"{rule.interval_days} day(s) between waterings."
            ),
            next_watering=next_scheduled,
        )

    if plant.expected_rain_mm >= rule.rain_threshold_mm:
        return EvaluationResult(
            plant_id=plant.plant_id,
            decision="postpone",
            reason=(
                f"{plant.expected_rain_mm} mm of rain is expected, at or above "
                f"the {rule.rain_threshold_mm} mm threshold."
            ),
            next_watering=today + timedelta(days=1),
        )

    return EvaluationResult(
        plant_id=plant.plant_id,
        decision="water",
        reason="Due for watering and not enough rain is expected.",
        next_watering=today,
    )
