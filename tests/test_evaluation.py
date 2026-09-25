"""Unit tests for the watering decision logic."""

from datetime import date

from app.models import Rule
from app.schemas import PlantEvaluation
from app.services.evaluation import evaluate_plant

VEGETABLE_RULE = Rule(plant_type="vegetable", interval_days=1, rain_threshold_mm=5.0)
TODAY = date(2026, 9, 25)


def test_no_rule_registered() -> None:
    """A plant type with no registered rule returns 'no_rule'."""
    plant = PlantEvaluation(
        plant_id=1, plant_type="cactus", last_watered_at=None, expected_rain_mm=0.0
    )

    result = evaluate_plant(plant, rule=None, today=TODAY)

    assert result.decision == "no_rule"
    assert result.next_watering is None


def test_never_watered_waters_today() -> None:
    """A plant that has never been watered should be watered today."""
    plant = PlantEvaluation(
        plant_id=1, plant_type="vegetable", last_watered_at=None, expected_rain_mm=0.0
    )

    result = evaluate_plant(plant, rule=VEGETABLE_RULE, today=TODAY)

    assert result.decision == "water"
    assert result.next_watering == TODAY


def test_within_interval_waits() -> None:
    """Watering before the rule's interval has elapsed waits."""
    plant = PlantEvaluation(
        plant_id=1, plant_type="vegetable", last_watered_at=TODAY, expected_rain_mm=0.0
    )

    result = evaluate_plant(plant, rule=VEGETABLE_RULE, today=TODAY)

    assert result.decision == "wait"
    assert result.next_watering == date(2026, 9, 26)


def test_expected_rain_postpones_watering() -> None:
    """Enough expected rain postpones watering by a day."""
    plant = PlantEvaluation(
        plant_id=1,
        plant_type="vegetable",
        last_watered_at=date(2026, 9, 20),
        expected_rain_mm=10.0,
    )

    result = evaluate_plant(plant, rule=VEGETABLE_RULE, today=TODAY)

    assert result.decision == "postpone"
    assert result.next_watering == date(2026, 9, 26)


def test_due_and_dry_waters() -> None:
    """Due for watering with no significant rain expected waters today."""
    plant = PlantEvaluation(
        plant_id=1,
        plant_type="vegetable",
        last_watered_at=date(2026, 9, 20),
        expected_rain_mm=0.0,
    )

    result = evaluate_plant(plant, rule=VEGETABLE_RULE, today=TODAY)

    assert result.decision == "water"
    assert result.next_watering == TODAY
