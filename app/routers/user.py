from fastapi import APIRouter, Response, Depends, status
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from .. import utils

router = APIRouter(
    prefix="/user", tags=["users"]
)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.User, db: Session = Depends(get_db)):

    hashed_password =  utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
