from fastapi import APIRouter
from .models import EventModel, EventListSchema, EventCreateSchema, EventUpdateSchema

from api.db.config import DATABASE_URL

router = APIRouter()


# /api/events/
@router.get("/")
def read_events() -> EventListSchema:
    import os

    print(os.environ.get("DATABASE_URL"), DATABASE_URL)
    # a bunch of items in a table
    return {
        "results": [{"id": i} for i in [1, 2, 3]],
        "count": 3
    }


@router.post("/")
def create_events(payload: EventCreateSchema) -> EventModel:
    data = payload.model_dump()
    return {"id": 123, **data}


@router.get("/{event_id}")
def get_event(event_id: int) -> EventModel:
    # a single row
    return {"id": event_id}


@router.put("/{event_id}")
def update_event(event_id: int, payload: EventUpdateSchema) -> EventModel:
    # a single row
    data = payload.model_dump()
    return {"id": event_id, **data}


@router.delete("/{event_id}")
def delete_event(event_id: int) -> EventModel:
    # a single row
    return {"id": event_id}
