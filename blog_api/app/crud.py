# crud.py
from models import User, Post, Comment, Category, Tag
from sqlalchemy import select, delete
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from schemas import UserCreate, UserUpdate, PostCreate, PostUpdate, PostStatus, CommentCreate, CommentUpdate, CategoryCreate, CategoryUpdate, TagCreate, TagUpdate, PostTagsUpdate
from typing import TypeVar, Optional
from security import hash_password # Import from the new security file

'''
Users CRUD
'''

def get_users(db: Session):
    stmt = select(User)
    result = db.execute(stmt)
    return result.scalars().all()

def insert_user(db: Session, user: UserCreate):
    new_user = User(**user.model_dump(exclude_unset=True))
    db.add(new_user)
    db.flush()
    return new_user

def get_user(db: Session, username: str) -> User:
    stmt = select(User).where(User.username == username)
    try:
        return db.execute(stmt).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
    except MultipleResultsFound:
        raise HTTPException(status_code=406, detail=f"Multiple users found with username '{username}'.")

def update_user(db: Session, username: str, user_update:UserUpdate):
    user = get_user(db, username)
    updt = user_update.model_dump(exclude_unset=True)
    if "password" in updt and updt["password"]:
        updt["password_hash"] = hash_password(updt.pop("password"))

    for col in updt:
        setattr(user, col, updt[col])
    db.flush()
    return user

def delete_user(db: Session, username: str) -> User:
    user_to_delete = get_user(db, username)
    db.delete(user_to_delete)
    db.flush()
    return user_to_delete
    
'''
Posts CRUD
'''

def get_posts(db: Session, skip: int = 0, limit: int = 10, status: Optional[PostStatus] = None):
    stmt = select(Post)
    if status:
        stmt = stmt.where(Post.status == status) 
    stmt = stmt.offset(skip).limit(limit) 
    result = db.execute(stmt)
    return result.scalars().all()

def get_post(db, id: int):
    try:
        stmt = select(Post).where(Post.id == id)
        result = db.execute(stmt)
        return result.scalars().one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Post not found ID:{id}")
    except MultipleResultsFound:
        raise HTTPException(status_code=409, detail=f"Multiple posts found with ID:{id}")

def insert_post(db: Session, post: PostCreate):
    new_post = Post(**post.model_dump(exclude_unset=True))
    db.add(new_post)
    db.flush()
    return new_post

def update_post(db: Session, post_id: int, post_update: PostUpdate):
    post = get_post(db, post_id)
    updt = post_update.model_dump(exclude_unset=True)
    for col in updt:
        setattr(post, col, updt[col])
    db.flush()
    return post

def assign_tags_to_post(db: Session, post_id: int, tags_update: PostTagsUpdate):
    post = get_post(db, post_id)
    tag_objects = [get_tag(db, id) for id in tags_update.tag_ids]
    post.tags = tag_objects
    db.flush()
    return post

def search_tag_posts(db: Session, tag_ids: list[int]):
    stmt = select(Post)
    stmt = stmt.join(Post.tags) 
    stmt = stmt.where(Tag.id.in_(tag_ids))
    stmt = stmt.distinct()
    return db.execute(stmt).scalars().all()
    
def search_category_posts(db: Session, category_ids: list[int]):
    stmt = select(Post)
    stmt = stmt.join(Post.category) 
    stmt = stmt.where(Category.id.in_(category_ids))
    stmt = stmt.distinct()
    return db.execute(stmt).scalars().all()

def delete_post(db: Session, post_id: int):
    post_to_delete = get_post(db, post_id)
    db.delete(post_to_delete)
    db.flush()
    return post_to_delete
    
'''
Comments CRUD
'''

def get_comments(db: Session):
    stmt = select(Comment)
    result = db.execute(stmt)
    return result.scalars().all()

def get_comment(db: Session, id: int):
    try:
        stmt = select(Comment).where(Comment.id == id)
        result = db.execute(stmt)
        return result.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Comment not found ID:{id}")
    except MultipleResultsFound:
        raise HTTPException(status_code=409, detail=f"Multiple comments found with ID:{id}")

def insert_comment(db: Session, comment: CommentCreate):
    new_comment = Comment(**comment.model_dump(exclude_unset=True))
    db.add(new_comment)
    db.flush()
    return new_comment

def update_comment(db: Session, comment_id: int, comment_update: CommentUpdate):
    comment = get_comment(db, comment_id)
    updt = comment_update.model_dump(exclude_unset=True)
    for col in updt:
        setattr(comment, col, updt[col])
    db.flush()
    
    return comment
    
def delete_comment(db: Session, comment_id: int):
    comment_to_delete = get_comment(db, comment_id)
    db.delete(comment_to_delete)
    db.flush()
    return comment_to_delete
    

'''
Categories CRUD
'''

def get_categories(db: Session):
    stmt = select(Category)
    result = db.execute(stmt)
    return result.scalars().all()
def get_category(db: Session, id: int):
    try:
        stmt = select(Category).where(Category.id == id)
        result = db.execute(stmt)
        return result.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Category with ID '{id}' not found")
    except MultipleResultsFound:
        raise HTTPException(status_code=409, detail=f"Multiple categories found with ID:{id}")
def insert_category(db: Session, category: CategoryCreate):
    new_category = Category(**category.model_dump(exclude_unset=True))
    db.add(new_category)
    db.flush()
    return new_category
def update_category(db: Session, category_id: int, category_update: CategoryUpdate):
    category = get_category(db, category_id)
    updt = category_update.model_dump(exclude_unset=True)
    for col in updt:
        setattr(category, col, updt[col])
    db.flush()
    
    return category

def get_post_comments(db: Session, post_id: int):
    stmt = select(Comment).where(Comment.post_id == post_id)
    return db.execute(stmt).scalars().all()

def get_post_author(db: Session, author_id: int):
    stmt = select(Post).where(Post.author_id == author_id)
    return db.execute(stmt).scalars().all()

def delete_category(db: Session, category_id: int):
    category_to_delete = get_category(db, category_id)
    db.delete(category_to_delete)
    db.flush()
    return category_to_delete
    
'''
Tags CRUD
'''

def get_tags(db: Session):
    stmt = select(Tag)
    result = db.execute(stmt)
    return result.scalars().all()
def get_tag(db: Session, id: int):
    try:
        stmt = select(Tag).where(Tag.id == id)
        result = db.execute(stmt)
        return result.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Tag with '{id}' not found")
    except MultipleResultsFound:
        raise HTTPException(status_code=409, detail=f"Multiple tags found with ID:{id}")
def insert_tag(db: Session, tag: TagCreate):
    new_tag = Tag(**tag.model_dump(exclude_unset=True))
    db.add(new_tag)
    db.flush()
    return new_tag
def update_tag(db: Session, tag_id: int, tag_update: TagUpdate):
    tag = get_tag(db, tag_id)
    updt = tag_update.model_dump(exclude_unset=True)
    for col in updt:
        setattr(tag, col, updt[col])
    db.flush()
    return tag
def delete_tag(db: Session, tag_id: int):
    tag_to_delete = get_tag(db, tag_id)
    db.delete(tag_to_delete)
    db.flush()
    return tag_to_delete