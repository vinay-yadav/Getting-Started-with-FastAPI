from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from starlette.responses import JSONResponse

app = FastAPI()


class NativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


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


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(None, title="Description of the Book", min_length=1, max_length=100)


BOOKS = []


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise raise_item_cannot_be_found_exception()


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise raise_item_cannot_be_found_exception()


@app.exception_handler(NativeNumberException)
async def native_number_exception_handler(request: Request, exc: NativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey, why do you want {exc.books_to_return} books. You need to read more."}
    )


# @app.post("/book/login")
# async def book_login(username: str = Form(), password: str = Form()):
#     return {"username": username, "password": password}


@app.post("/book/login")
async def book_login(book_id: int, username: str = Header(None), password: str = Header(None)):
    if username == "FastAPIUser" and password == "test1234!":
        if len(BOOKS) < 1:
            create_books_no_api()
        return BOOKS[book_id]
    return "Invalid User"


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NativeNumberException(books_to_return)

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


@app.post("/", status_code=status.HTTP_201_CREATED)
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

    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return "Book with ID {} was deleted".format(book_id)

    # raise HTTPException(
    #     status_code=404, detail="Book with ID {} was not found".format(book_id),
    #     headers={"X-Header-Error": "Nothing to be seen at the UUID"}
    # )

    raise raise_item_cannot_be_found_exception()


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


def raise_item_cannot_be_found_exception():
    raise HTTPException(
        status_code=404, detail="Book not found", headers={"X-Header-Error": "Nothing to be seen at the UUID"}
    )
