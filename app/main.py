from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from . import schemas
from . import utils
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#dependency
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally : 
        db.close()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)