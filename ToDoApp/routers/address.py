import sys

sys.path.append("..")

import models
from typing import Optional
from fastapi import APIRouter, Depends
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/address",
    tags=["address"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        db.close()


class Address(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str


@router.post("/")
async def create_address(address: Address, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise get_user_exception()

    address_model = models.Address(
        address1=address.address1,
        address2=address.address2,
        city=address.city,
        state=address.state,
        country=address.country,
        postalcode=address.postalcode
    )

    db.add(address_model)
    db.flush()

    user_model = db.query(models.User).filter(models.User.id == user.get("id")).first()
    user_model.address_id = address_model.id

    db.add(user_model)
    db.commit()
