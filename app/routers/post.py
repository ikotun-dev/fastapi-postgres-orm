from fastapi import APIRouter, Response, Depends, status, HTTPException
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2
from typing import List

router = APIRouter(
    prefix="/posts", tags=["posts"]
)

@router.post("/")
def create_post(post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post =  models.Post(user_id = current_user.id , **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(current_user)

    return {'data' : new_post}

@router.get("/{id}", response_model=schemas.PostOut)
def get_posts(id: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")

    if post.user_id != current_user.id:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to get this post")

    return post

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10):
    posts = db.query(models.Post).limit(limit).all()
    if not posts : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")

    # if post.user_id != current_user.id:
    #     return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to get this post")

    return posts

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
     post = db.query(models.Post).filter(models.Post.id == id)
     if post.first() == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")

     post.delete(synchronize_session=False)
     db.commit()
     return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")  
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post.user_id != current_user.id:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    post_query.update(updated_post.dict(), synchronize_session=False)
    return {'data' : updated_post}

