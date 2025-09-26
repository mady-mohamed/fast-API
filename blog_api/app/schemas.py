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
    
T = TypeVar("T", bound=UserBase)

class OptionalUModel(UserBase, Generic[T]):
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        for field_name, field in cls.model_fields.items():
            field.annotation = Optional[field.annotation]
            field.default = None
            
class UserUpdate(OptionalUModel[UserBase]):
    pass

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
    
T = TypeVar("T", bound=PostBase)

class OptionalPModel(PostBase, Generic[T]):
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        for field_name, field in cls.model_fields.items():
            field.annotation = Optional[field.annotation]
            field.default = None
            
class PostUpdate(OptionalPModel[PostBase]):
    pass

class PostCreate(PostBase):
    author_id: int

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

T = TypeVar("T", bound=CommentBase)

class OptionalCModel(CommentBase, Generic[T]):
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        for field_name, field in cls.model_fields.items():
            field.annotation = Optional[field.annotation]
            field.default = None
            
class CommentUpdate(OptionalCModel[CommentBase]):
    pass

class CommentResponse(CommentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Category & Tag
class CategoryBase(BaseModel):
    name: str
    slug: Optional[str]

class CategoryCreate(CategoryBase):
    pass

T = TypeVar("T", bound=CategoryBase)

class OptionalcModel(CategoryBase, Generic[T]):
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        for field_name, field in cls.model_fields.items():
            field.annotation = Optional[field.annotation]
            field.default = None
            
class CategoryUpdate(OptionalcModel[CategoryBase]):
    pass

class CategoryResponse(CategoryBase):
    id: int
    name: str
    class Config:
        orm_mode = True

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

T = TypeVar("T", bound=TagBase)

class OptionalTModel(TagBase, Generic[T]):
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        for field_name, field in cls.model_fields.items():
            field.annotation = Optional[field.annotation]
            field.default = None
            
class TagUpdate(OptionalTModel[TagBase]):
    pass

class TagResponse(TagBase):
    id: int
    name: str
    class Config:
        orm_mode = True
