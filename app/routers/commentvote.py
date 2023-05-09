from fastapi import FastAPI, HTTPException, Depends, APIRouter, status, Response
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/commentvotes",
    tags=['Comment Votes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.CommentVote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment = db.query(models.Comment).filter(
        models.Comment.id == vote.comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment does not exist")

    vote_query = db.query(models.CommentVote).filter(
        models.CommentVote.comment_id == vote.comment_id, models.CommentVote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on comment {vote.comment_id}")
        new_vote = models.CommentVote(
            comment_id=vote.comment_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "deleted vote"}
