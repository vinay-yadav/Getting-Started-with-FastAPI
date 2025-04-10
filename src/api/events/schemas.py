from typing import List

from pydantic import BaseModel


class EventCreateSchema(BaseModel):
    page: str


class EventUpdateSchema(BaseModel):
    description: str


class EventSchema(BaseModel):
    id: int

# {"id": 123}

class EventListSchema(BaseModel):
    results: List[EventSchema]
    count: int
