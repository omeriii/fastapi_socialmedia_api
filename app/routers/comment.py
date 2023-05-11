from fastapi import FastAPI, HTTPException, Depends, APIRouter, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/comments",
    tags=['Comments']
)


@router.get("/", response_model=List[schemas.CommentOut])
def get_comments(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100):

    # comments = db.query(models.Comment).limit(limit).all()
    comments = db.query(models.Comment, func.count(models.CommentVote.comment_id).label("votes")).join(
        models.CommentVote, models.CommentVote.comment_id == models.Comment.id, isouter=True).group_by(models.Comment.id).limit(limit).all()
    return comments


@router.get("/{id}", response_model=schemas.CommentOut)
def get_comment(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    comment = db.query(models.Comment, func.count(models.CommentVote.comment_id).label("votes")).join(
        models.CommentVote, models.CommentVote.comment_id == models.Comment.id, isouter=True).group_by(models.Comment.id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {id} was not found")
    return comment


@router.get("/user/{user_id}", response_model=List[schemas.CommentOut])
def get_comments_of_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100):

    # comments = db.query(models.Comment).limit(limit).all()
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    comments = db.query(models.Comment, func.count(models.CommentVote.comment_id).label("votes")).join(
        models.CommentVote, models.CommentVote.comment_id == models.Comment.id, isouter=True).group_by(models.Comment.id).filter(models.Comment.user_id == user_id).limit(limit).all()
    return comments


@router.get("/post/{post_id}", response_model=List[schemas.CommentOut])
def get_comments_of_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100):

    # comments = db.query(models.Comment).limit(limit).all()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    comments = db.query(models.Comment, func.count(models.CommentVote.comment_id).label("votes")).join(
        models.CommentVote, models.CommentVote.comment_id == models.Comment.id, isouter=True).group_by(models.Comment.id).filter(models.Comment.post_id == post_id).limit(limit).all()
    return comments


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_comment = models.Comment(user_id=current_user.id, **comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == id)

    comment = comment_query.first()

    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {id} does not exist")

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    comment_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Comment)
def update_post(id: int, updated_comment: schemas.CommentPut, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    comment = comment_query.first()

    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {id} does not exist")

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    comment_query.update(updated_comment.dict(), synchronize_session=False)
    db.commit()
    return comment_query.first()
