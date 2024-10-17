import models

from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    title: str
    description: str = Optional[str]
    priority: int = Field(gt=0, lt=6, description='Priority of the task')
    completed: bool


@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.ToDo).all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise http_exception()


@app.post("/")
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = models.ToDo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        completed=todo.completed
    )
    db.add(todo_model)
    db.commit()

    return successful_response(201)


@app.put("/{todo_id}")
async def update_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    todo_model = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()

    if todo_model is None:
        raise http_exception()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.completed = todo.completed

    db.add(todo_model)
    db.commit()
    return successful_response(202)


@app.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if todo_model is None:
        raise http_exception()

    db.delete(todo_model)
    db.commit()
    return successful_response(202)


def successful_response(status_code: int):
    return {"status_code": status_code, "transaction": "successful"}


def http_exception():
    return HTTPException(status_code=404, detail="ToDo not found")
