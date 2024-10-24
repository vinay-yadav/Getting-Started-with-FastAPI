import models

from fastapi import FastAPI, Depends
from database import engine
from routers import auth, todos
from company import companyapis, dependencies

app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(
    companyapis.router,
    prefix="/companyapis",
    tags=["companyapis"],
    dependencies=[Depends(dependency=dependencies.get_token_header)],
    responses={404: {"description": "Not found"}},
)

models.Base.metadata.create_all(bind=engine)
