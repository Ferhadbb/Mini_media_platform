import uuid
from pydantic import BaseModel
from datetime import datetime
from app.api.v1.schemas.user import UserOut

class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostOut(PostBase):
    id: uuid.UUID
    created_at: datetime
    owner: UserOut
    likes_count: int

    class Config:
        from_attributes = True 