import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services import user_service
from app.api.v1.schemas.user import UserProfile

router = APIRouter()


@router.get("/me", response_model=UserProfile, status_code=status.HTTP_200_OK)
def read_users_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {
        **current_user.__dict__,
        "followers_count": len(current_user.followers),
        "following_count": len(current_user.following),
        "is_following": False,
    }


@router.get("/{user_id}", response_model=UserProfile, status_code=status.HTTP_200_OK)
def read_user(user_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = user_service.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    is_following = user_service.is_following(db, follower_id=current_user.id, followed_id=user_id)
    
    return {
        **user.__dict__,
        "followers_count": len(user.followers),
        "following_count": len(user.following),
        "is_following": is_following,
    }


@router.post("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
def follow_user(user_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_to_follow = user_service.get_user(db, user_id=user_id)
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="User not found")
    if user_service.is_following(db, follower_id=current_user.id, followed_id=user_id):
        raise HTTPException(status_code=400, detail="Already following")

    user_service.follow_user(db, follower_id=current_user.id, followed_id=user_id)


@router.delete("/{user_id}/unfollow", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(user_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_to_unfollow = user_service.get_user(db, user_id=user_id)
    if not user_to_unfollow:
        raise HTTPException(status_code=404, detail="User not found")
    if not user_service.is_following(db, follower_id=current_user.id, followed_id=user_id):
        raise HTTPException(status_code=400, detail="Not following")

    user_service.unfollow_user(db, follower_id=current_user.id, followed_id=user_id)
