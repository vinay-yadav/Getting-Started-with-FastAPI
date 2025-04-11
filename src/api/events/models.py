from typing import List, Optional

from sqlmodel import Field, SQLModel


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = ""
    description: Optional[str] = ""


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="My description")


class EventUpdateSchema(SQLModel):
    page: Optional[str] = ""
    description: str

# {"id": 123}

class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int
