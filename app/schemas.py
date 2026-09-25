"""Request and response schemas for the watering-api."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Decision = Literal["water", "postpone", "wait", "no_rule"]


class RuleOut(BaseModel):
    """Watering rule returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    plant_type: str = Field(examples=["vegetable"])
    interval_days: int = Field(examples=[1])
    rain_threshold_mm: float = Field(examples=[5.0])


class RuleIn(BaseModel):
    """Payload to create a watering rule."""

    plant_type: str = Field(examples=["vegetable"])
    interval_days: int = Field(gt=0, examples=[1])
    rain_threshold_mm: float = Field(ge=0, examples=[5.0])


class RuleUpdate(BaseModel):
    """Payload to update a watering rule's interval and rain threshold."""

    interval_days: int = Field(gt=0, examples=[1])
    rain_threshold_mm: float = Field(ge=0, examples=[5.0])


class PlantEvaluation(BaseModel):
    """One plant to evaluate against its watering rule."""

    plant_id: int = Field(examples=[1])
    plant_type: str = Field(examples=["vegetable"])
    last_watered_at: date | None = Field(default=None, examples=["2026-09-20"])
    expected_rain_mm: float = Field(ge=0, examples=[0.0])


class EvaluationRequest(BaseModel):
    """Batch of plants to evaluate."""

    plants: list[PlantEvaluation]


class EvaluationResult(BaseModel):
    """Watering decision for one plant."""

    plant_id: int
    decision: Decision
    reason: str
    next_watering: date | None


class EvaluationResponse(BaseModel):
    """Watering decisions for a batch of plants."""

    evaluations: list[EvaluationResult]
