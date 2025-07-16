from fastapi import FastAPI, status
from app.api.v1.routers import auth, users, posts, likes
from app.core.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Social Network API")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(likes.router, prefix="/posts", tags=["likes"])


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "Welcome!"}
