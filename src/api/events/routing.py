from fastapi import APIRouter
from .schemas import EventSchema, EventListSchema, EventCreateSchema, EventUpdateSchema

router = APIRouter()


# /api/events/
@router.get("/")
def read_events() -> EventListSchema:
    # a bunch of items in a table
    return {
        "results": [{"id": i} for i in [1, 2, 3]],
        "count": 3
    }


@router.post("/")
def create_events(payload: EventCreateSchema) -> EventSchema:
    print(payload)
    return {"id": 123}


@router.get("/{event_id}")
def get_event(event_id: int) -> EventSchema:
    # a single row
    return {"id": event_id}


@router.put("/{event_id}")
def update_event(event_id: int, payload: EventUpdateSchema) -> EventSchema:
    # a single row
    print(payload)
    return {"id": event_id}


@router.delete("/{event_id}")
def delete_event(event_id: int) -> EventSchema:
    # a single row
    return {"id": event_id}
