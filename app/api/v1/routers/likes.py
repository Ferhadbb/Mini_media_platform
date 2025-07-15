import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services import post_service

router = APIRouter()


@router.post("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def like_post(
    post_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = post_service.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    try:
        post_service.like_post(db, user_id=current_user.id, post_id=post_id)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Post already liked")


@router.delete("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(
    post_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = post_service.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    like = post_service.unlike_post(db, user_id=current_user.id, post_id=post_id)
    if not like:
        raise HTTPException(status_code=400, detail="Post not liked")
