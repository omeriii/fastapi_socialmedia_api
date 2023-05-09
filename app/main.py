from fastapi import FastAPI
# import app.models as models
# from app.database import engine
from .routers import post, user, auth, vote, comment, commentvote

# add CORSMiddleware
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(comment.router)
app.include_router(commentvote.router)
