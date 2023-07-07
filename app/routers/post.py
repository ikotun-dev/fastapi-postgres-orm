from fastapi import APIRouter, Response, Depends, status
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/posts", tags=["posts"]
)

@router.post("/")
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    new_post =  models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'data' : new_post}

@router.get("/{id}")
def get_posts(id: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    print(post)
    if not post : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return {'data' : post}

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
     post = db.query(models.Post).filter(models.Post.id == id)
     if post.first() == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")

     post.delete(synchronize_session=False)
     db.commit()
     return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")  
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_query.update(updated_post.dict(), synchronize_session=False)
    return {'data' : updated_post}
