from fastapi import FastAPI, HTTPException, status, Response, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from . import schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#dependency
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally : 
        db.close()


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data' : posts}

@app.post("/sqlalchemy")
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    new_post =  models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'data' : new_post}

@app.get("/sqlalchemy/{id}")
def get_posts(id: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    print(post)
    if not post : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return {'data' : post}

@app.delete("/sqlalchemy/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
     post = db.query(models.Post).filter(models.Post.id == id)
     if post.first() == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")

     post.delete(synchronize_session=False)
     db.commit()
     return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/sqlalchemy/{id}")  
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_query.update(updated_post.dict(), synchronize_session=False)
    return {'data' : updated_post}


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.User, db: Session = Depends(get_db)):

    hashed_password =  pwd_context.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


