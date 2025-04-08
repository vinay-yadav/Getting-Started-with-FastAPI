from typing import List

from pydantic import BaseModel


class EventSchema(BaseModel):
    id: int

# {"id": 123}

class EventListSchema(BaseModel):
    results: List[EventSchema]
    count: int
