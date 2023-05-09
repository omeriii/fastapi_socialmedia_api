from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class Comment(BaseModel):
    id: int
    body: str
    created_at: datetime
    user_id: int
    post_id: int

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    body: str
    post_id: int


class CommentPut(BaseModel):
    body: str


class Comment(BaseModel):
    id: int
    body: str
    created_at: datetime
    user_id: int
    post_id: int
    user: UserOut
    post: PostBase

    class Config:
        orm_mode = True


class CommentOut(BaseModel):
    Comment: Comment
    votes: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class CommentVote(BaseModel):
    comment_id: int
    dir: conint(le=1)
