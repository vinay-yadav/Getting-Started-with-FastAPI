from typing import Optional

from fastapi import FastAPI
from enum import Enum

app = FastAPI()

# BOOKS = [
#     {"book_1": {'title': 'Title One', 'author': 'Author One', 'category': 'science'}},
#     {"book_2": {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'}},
#     {"book_3": {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'}},
#     {"book_4": {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'}},
#     {"book_5": {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'}},
#     {"book_6": {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}}
# ]

BOOKS = {
    "book_1": {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    "book_2": {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    "book_3": {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    "book_4": {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    "book_5": {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    "book_6": {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
}


class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    new_books = BOOKS.copy()
    if not skip_book:
        return new_books

    del new_books[skip_book]
    return new_books


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {"book_id": book_id}


@app.get("/{book_name}")
async def read_book_by_name(book_name: str):
    return BOOKS[book_name]


@app.post("/")
async def create_book(book_title: str, author: str, category: str):
    book_id = len(BOOKS) + 1
    BOOKS[book_id] = {"title": book_title, "author": author, "category": category}
    return BOOKS[book_id]


@app.put("/{book_id}")
async def update_book(book_id: str, book_title: str, author: str, category: str):
    BOOKS[book_id]["title"] = book_title
    BOOKS[book_id]["author"] = author
    BOOKS[book_id]["category"] = category
    return BOOKS[book_id]


@app.delete("/{book_name}")
async def delete_book(book_name: str):
    del BOOKS[book_name]
    return f"Book {book_name} deleted"


@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        sub = "Up"
    elif direction_name == DirectionName.south:
        sub = "Down"
    elif direction_name == DirectionName.east:
        sub = "Right"
    else:
        sub = "Left"

    return {"direction_name": direction_name, "sub": sub}
