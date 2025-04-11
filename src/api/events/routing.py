from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .models import EventModel, EventListSchema, EventCreateSchema, EventUpdateSchema

from api.db.config import DATABASE_URL
from api.db.session import get_session

router = APIRouter()


# /api/events/
@router.get("/", response_model=EventListSchema)
def read_events(session: Session = Depends(get_session)):
    # a bunch of items in a table
    query = select(EventModel).order_by(EventModel.id.desc()).limit(10)
    results = session.exec(query).all()
    return {
        "results": results,
        "count": len(results)
    }


@router.post("/", response_model=EventModel)
def create_events(payload: EventCreateSchema, session: Session = Depends(get_session)):
    data = payload.model_dump()
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result


@router.put("/{event_id}", response_model=EventModel)
def update_event(event_id: int, payload: EventUpdateSchema, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")

    data = payload.model_dump()

    for k, v in data.items():
        setattr(obj, k, v)

    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.delete("/{event_id}")
def delete_event(event_id: int) -> EventModel:
    # a single row
    return {"id": event_id}
