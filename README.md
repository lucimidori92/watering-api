# watering-api

Secondary API of the **Smart Garden** MVP (PUC Software Architecture course).
Owns the watering rules per plant type and decides whether a plant should be
watered, have its watering postponed, wait, or flag a missing rule.

Main component: [garden-main-api](https://github.com/lucimidori92/garden-main-api)

## How the decision is made

Given a plant's type, its last watering date and the rain expected for it,
`POST /evaluations` applies these rules in order:

1. No rule registered for the plant type → `no_rule`.
2. Never watered before → `water`.
3. Fewer days than the rule's interval have passed since the last watering →
   `wait`, with the next scheduled watering date.
4. Expected rain meets or exceeds the rule's threshold → `postpone`.
5. Otherwise → `water`.

## Running with Docker

This service is normally started together with `garden-main-api` through its
`docker-compose.yml`. To run it on its own:

```bash
docker build -t watering-api .
docker run -p 8001:8001 watering-api
```

Swagger UI: <http://localhost:8001/docs>

## Running without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8001
```

Run the tests (in `tests/`, kept out of the Docker image):

```bash
pytest
```

## Routes

| Method | Route | Description |
|---|---|---|
| GET | `/rules` | List all watering rules |
| POST | `/rules` | Create a rule (409 if the plant type already has one) |
| PUT | `/rules/{plant_type}` | Update a rule's interval and rain threshold (404 if missing) |
| DELETE | `/rules/{plant_type}` | Delete a rule (404 if missing) |
| POST | `/evaluations` | Evaluate a batch of plants and return a watering decision for each |
