from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(alias="Title", min_length=1)
    author: str = Field(alias="Author", min_length=1)
    description: Optional[str] = Field(alias="Description", title="Description of the Book", min_length=1, max_length=100)
    rating: int = Field(alias="Rating", ge=0, le=5)


BOOKS = []


@app.get("/")
async def read_all_books():
    return BOOKS


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book
