from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from .. import models
from .. import utils

router = APIRouter()

@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    return {'token' : 'example token'}
    
      