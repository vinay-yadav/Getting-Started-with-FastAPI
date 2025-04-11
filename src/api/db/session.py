import sqlmodel
from sqlmodel import SQLModel
from .config import DATABASE_URL

if DATABASE_URL == "":
    raise NotImplementedError("Database URL needs to be set")

engine = sqlmodel.create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)
