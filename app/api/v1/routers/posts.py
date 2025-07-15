import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services import post_service
from app.api.v1.schemas.post import PostCreate, PostUpdate, PostOut

router = APIRouter()


@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_post = post_service.create_post(db=db, post=post, owner_id=current_user.id)
    return {**new_post.__dict__, "owner": current_user, "likes_count": 0}


@router.get("/", response_model=List[PostOut], status_code=status.HTTP_200_OK)
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts_with_likes = post_service.get_posts_with_like_count(db, skip=skip, limit=limit)
    return [
        {**post.__dict__, "owner": post.owner, "likes_count": likes_count}
        for post, likes_count in posts_with_likes
    ]


@router.get("/{post_id}", response_model=PostOut, status_code=status.HTTP_200_OK)
def read_post(post_id: uuid.UUID, db: Session = Depends(get_db)):
    result = post_service.get_post_with_like_count(db, post_id=post_id)
    if not result:
        raise HTTPException(status_code=404, detail="Post not found")
    post, likes_count = result
    return {**post.__dict__, "owner": post.owner, "likes_count": likes_count}


@router.put("/{post_id}", response_model=PostOut, status_code=status.HTTP_200_OK)
def update_post(
    post_id: uuid.UUID,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = post_service.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    updated_post = post_service.update_post(db, post=post, update_data=post_update)
    return {
        **updated_post.__dict__,
        "owner": current_user,
        "likes_count": len(updated_post.likes),
    }


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = post_service.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    post_service.delete_post(db, post=post)
