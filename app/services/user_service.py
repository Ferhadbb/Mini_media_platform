import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.follow import Follow

def get_user(db: Session, user_id: uuid.UUID) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def follow_user(db: Session, follower_id: uuid.UUID, followed_id: uuid.UUID):
    if follower_id == followed_id:
        return None
    db_follow = Follow(follower_id=follower_id, followed_id=followed_id)
    db.add(db_follow)
    db.commit()
    return db_follow

def unfollow_user(db: Session, follower_id: uuid.UUID, followed_id: uuid.UUID):
    db_follow = db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.followed_id == followed_id
    ).first()
    if db_follow:
        db.delete(db_follow)
        db.commit()
    return db_follow

def is_following(db: Session, follower_id: uuid.UUID, followed_id: uuid.UUID) -> bool:
    return db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.followed_id == followed_id
    ).first() is not None 