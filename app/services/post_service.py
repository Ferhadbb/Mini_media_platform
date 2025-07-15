import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Post, Like
from app.api.v1.schemas.post import PostCreate, PostUpdate

def create_post(db: Session, post: PostCreate, owner_id: uuid.UUID) -> Post:
    db_post = Post(**post.dict(), owner_id=owner_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db: Session, post_id: uuid.UUID) -> Optional[Post]:
    return db.query(Post).filter(Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    return db.query(Post).offset(skip).limit(limit).all()

def update_post(db: Session, post: Post, update_data: PostUpdate) -> Post:
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post: Post):
    db.delete(post)
    db.commit()

def like_post(db: Session, user_id: uuid.UUID, post_id: uuid.UUID) -> Optional[Like]:
    db_like = Like(user_id=user_id, post_id=post_id)
    db.add(db_like)
    db.commit()
    return db_like

def unlike_post(db: Session, user_id: uuid.UUID, post_id: uuid.UUID):
    db_like = db.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).first()
    if db_like:
        db.delete(db_like)
        db.commit()
    return db_like

def get_post_with_like_count(db: Session, post_id: uuid.UUID):
    return db.query(
        Post,
        func.count(Like.post_id).label("likes_count")
    ).outerjoin(Like, Post.id == Like.post_id).filter(Post.id == post_id).group_by(Post.id).first()

def get_posts_with_like_count(db: Session, skip: int = 0, limit: int = 100):
    return db.query(
        Post,
        func.count(Like.post_id).label("likes_count")
    ).outerjoin(Like, Post.id == Like.post_id).group_by(Post.id).offset(skip).limit(limit).all() 