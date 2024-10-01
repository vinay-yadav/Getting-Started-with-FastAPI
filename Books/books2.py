from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the Book", min_length=1, max_length=100)
    rating: int = Field(ge=0, le=5)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "8b0ac3ce-9fe2-4b31-9a1d-0727246a7dab",
                "title": "Book",
                "author": "Vinay",
                "description": "The book was written by Vinay",
                "rating": 5,
            }
        }


BOOKS = []


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if len(BOOKS) < 1:
        create_books_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = list()
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return "Book with ID {} was deleted".format(book_id)


def create_books_no_api():
    book_1 = Book(
        id="0b0ac3ce-9fe2-4b31-9a1d-0727246a7dab", title="Title 1", author="Author 1",
        description="Description 1", rating=2
    )
    book_2 = Book(
        id="1b0ac3ce-9fe2-4b31-9a1d-0727246a7dab", title="Title 2", author="Author 2",
        description="Description 2", rating=4
    )
    book_3 = Book(
        id="2b0ac3ce-9fe2-4b31-9a1d-0727246a7dab", title="Title 3", author="Author 3",
        description="Description 3", rating=3
    )
    book_4 = Book(
        id="3b0ac3ce-9fe2-4b31-9a1d-0727246a7dab", title="Title 4", author="Author 4",
        description="Description 4", rating=5
    )

    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
