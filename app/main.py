"""Entry point for the watering-api."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import SessionLocal, init_db
from app.routers import evaluations, rules
from app.seed import create_default_rules


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Prepares the database and default rules before the API accepts requests.

    Args:
        _app: FastAPI application (unused).

    Yields:
        Control back to FastAPI while the API is running.
    """
    init_db()
    with SessionLocal() as session:
        create_default_rules(session)
    yield


app = FastAPI(
    title="watering-api",
    description="Smart Garden's secondary API: watering rules per plant type "
    "and the decision to water, postpone or wait.",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(rules.router)
app.include_router(evaluations.router)


@app.get("/")
def root() -> dict[str, str]:
    """Greets whoever hits the API root and points them to the docs.

    Returns:
        A welcome message and the interactive docs URL.
    """
    return {"message": "💧 watering-api is running! Docs at /docs."}
