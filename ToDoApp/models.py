from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship('ToDo', back_populates='owner')


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="todos")

# insert into todos (title, description, priority, completed) values ("Go to the store", "Pick-up eggs", 5, False)
# insert into todos (title, description, priority, completed) values ("Cut the lawn", "Grass is getting long", 3, False)
# insert into todos (title, description, priority, completed) values ("Feed the dog", "He is getting hungry", 5, False)
# insert into todos (title, description, priority, completed) values ("Test element", "He is getting hungry", 5, False)
