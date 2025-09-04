from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class PostStatus(str, Enum):
    draft = "draft"
    published = "published"

# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]

class UserCreate(UserBase):
    password: str   # raw password for registration

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_admin: bool

    class Config:
        orm_mode = True

# Post schemas
class PostBase(BaseModel):
    title: str
    slug: str
    content: str
    status: PostStatus

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    publication_date: datetime
    author_id: int

    class Config:
        orm_mode = True

# Comment schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    author_id: int
    post_id: int

    class Config:
        orm_mode = True

# Category & Tag
class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    class Config:
        orm_mode = True

class TagResponse(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True
