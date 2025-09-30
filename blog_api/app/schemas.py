from pydantic import BaseModel
from typing import Optional, TypeVar, Generic, Any
from datetime import datetime
from enum import Enum

class Token(BaseModel):
    access_token: str
    token_type: str

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
    password: str   # hash password later for registration (only at creation)
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None # Will be hashed if provided
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    is_admin: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_admin: bool

    class Config:
        orm_mode = True

# Post schemas
class PostBase(BaseModel):
    title: str
    slug: Optional[str]
    content: str
    status: PostStatus
    category_id: int

class PostCreate(PostBase):
    author_id: int

class PostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    status: Optional[PostStatus] = None
    category_id: Optional[int] = None

class PostResponse(PostBase):
    id: int
    publication_date: datetime
    author_id: int
    category_id: int

    class Config:
        orm_mode = True

# Comment schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    author_id: int
    post_id: int

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    author_id: int
    post_id: int

    class Config:
        orm_mode = True

# Category & Tag
class CategoryBase(BaseModel):
    name: str
    slug: Optional[str]

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    name: str
    class Config:
        orm_mode = True

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = None

class TagResponse(TagBase):
    id: int
    name: str
    class Config:
        orm_mode = True