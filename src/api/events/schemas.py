from typing import List, Optional

from pydantic import BaseModel, Field


class EventCreateSchema(BaseModel):
    page: str
    description: Optional[str] = Field(default="My description")


class EventUpdateSchema(BaseModel):
    page: Optional[str] = ""
    description: str


class EventSchema(BaseModel):
    id: int
    page: Optional[str] = ""
    description: Optional[str] = ""

# {"id": 123}

class EventListSchema(BaseModel):
    results: List[EventSchema]
    count: int
