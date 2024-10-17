from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from database import Base


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)

# insert into todos (title, description, priority, completed) values ("Go to the store", "Pick-up eggs", 5, False)
# insert into todos (title, description, priority, completed) values ("Cut the lawn", "Grass is getting long", 3, False)
# insert into todos (title, description, priority, completed) values ("Feed the dog", "He is getting hungry", 5, False)
# insert into todos (title, description, priority, completed) values ("Test element", "He is getting hungry", 5, False)