from fastapi import APIRouter, Response, Depends, status, HTTPException
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2
from typing import List

router = APIRouter(
    prefix="/vote", tags=["posts"]
)


@router.post("/")
def like_post(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    db_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    found_vote = db_query.first()
    if (vote.like_dir == 1) : 
        if found_vote:
             return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user has voted on post before')
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'vote does not exist')
        db_query.delete(synchronize_session=False)
        db.commit()
        return  {'message' : 'post has been unliked'}
     


          
            
    
