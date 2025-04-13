import sqlmodel
from datetime import datetime, timezone
from typing import List, Optional
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now

from sqlmodel import Field, SQLModel


# def get_utc_now() -> datetime:
#     return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

# page visits at any given time

class EventModel(TimescaleModel, table=True):
    page: str = Field(index=True)
    description: Optional[str] = ""
    updated_at: datetime = Field(
        default_factory=get_utc_now, sa_type=sqlmodel.DateTime(timezone=True), nullable=False
    )

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"
    
    # id: Optional[int] = Field(default=None, primary_key=True)
    # created_at: datetime = Field(
    #     default_factory=get_utc_now, sa_type=sqlmodel.DateTime(timezone=True), nullable=False
    # )


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
