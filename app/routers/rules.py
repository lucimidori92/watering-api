"""Watering rule routes."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import Rule
from app.schemas import RuleOut

router = APIRouter(prefix="/rules", tags=["Rules"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("", response_model=list[RuleOut], summary="List watering rules")
def list_rules(session: SessionDep) -> list[Rule]:
    """Lists all registered watering rules.

    Args:
        session: Database session injected by FastAPI.

    Returns:
        Rules ordered by plant type.
    """
    return list(session.scalars(select(Rule).order_by(Rule.plant_type)))
