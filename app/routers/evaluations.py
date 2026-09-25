"""Watering evaluation routes."""

from datetime import datetime
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import Rule
from app.schemas import EvaluationRequest, EvaluationResponse
from app.services.evaluation import evaluate_plant

router = APIRouter(prefix="/evaluations", tags=["Evaluations"])

SessionDep = Annotated[Session, Depends(get_session)]
TIMEZONE = ZoneInfo("America/Sao_Paulo")


@router.post(
    "", response_model=EvaluationResponse, summary="Evaluate a batch of plants"
)
def evaluate_plants(
    request: EvaluationRequest, session: SessionDep
) -> EvaluationResponse:
    """Decides whether to water, postpone or wait for each plant in the batch.

    Args:
        request: The plants to evaluate.
        session: Database session injected by FastAPI.

    Returns:
        One watering decision per plant, in the same order as the request.
    """
    today = datetime.now(TIMEZONE).date()
    rules = {rule.plant_type: rule for rule in session.scalars(select(Rule))}
    evaluations = [
        evaluate_plant(plant, rules.get(plant.plant_type), today)
        for plant in request.plants
    ]
    return EvaluationResponse(evaluations=evaluations)
