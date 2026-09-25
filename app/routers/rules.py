"""Watering rule routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import Rule
from app.schemas import RuleIn, RuleOut, RuleUpdate

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


@router.post(
    "",
    response_model=RuleOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a watering rule",
)
def create_rule(rule_in: RuleIn, session: SessionDep) -> Rule:
    """Creates a watering rule for a plant type.

    Args:
        rule_in: The rule to create.
        session: Database session injected by FastAPI.

    Returns:
        The created rule.

    Raises:
        HTTPException: 409 if a rule already exists for that plant type.
    """
    if session.get(Rule, rule_in.plant_type) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A rule already exists for plant type '{rule_in.plant_type}'.",
        )
    rule = Rule(**rule_in.model_dump())
    session.add(rule)
    session.commit()
    session.refresh(rule)
    return rule


@router.put("/{plant_type}", response_model=RuleOut, summary="Update a watering rule")
def update_rule(plant_type: str, rule_update: RuleUpdate, session: SessionDep) -> Rule:
    """Updates the interval and rain threshold of an existing rule.

    Args:
        plant_type: The plant type whose rule is being updated.
        rule_update: The new interval and rain threshold.
        session: Database session injected by FastAPI.

    Returns:
        The updated rule.

    Raises:
        HTTPException: 404 if no rule exists for that plant type.
    """
    rule = session.get(Rule, plant_type)
    if rule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No rule found for plant type '{plant_type}'.",
        )
    rule.interval_days = rule_update.interval_days
    rule.rain_threshold_mm = rule_update.rain_threshold_mm
    session.commit()
    session.refresh(rule)
    return rule


@router.delete(
    "/{plant_type}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a watering rule",
)
def delete_rule(plant_type: str, session: SessionDep) -> None:
    """Deletes the watering rule for a plant type.

    Args:
        plant_type: The plant type whose rule is being deleted.
        session: Database session injected by FastAPI.

    Raises:
        HTTPException: 404 if no rule exists for that plant type.
    """
    rule = session.get(Rule, plant_type)
    if rule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No rule found for plant type '{plant_type}'.",
        )
    session.delete(rule)
    session.commit()
