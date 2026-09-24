"""Request and response schemas for the watering-api."""

from pydantic import BaseModel, ConfigDict, Field


class RuleOut(BaseModel):
    """Watering rule returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    plant_type: str = Field(examples=["vegetable"])
    interval_days: int = Field(examples=[1])
    rain_threshold_mm: float = Field(examples=[5.0])
