from models import User, Post, Comment, Category, Tag
from sqlalchemy import select, delete
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from schemas import UserCreate, UserUpdate, PostCreate, PostUpdate, CommentCreate, CommentUpdate, CategoryCreate, CategoryUpdate, TagCreate, TagUpdate
from typing import TypeVar

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
    db.commit()
    return new_user.id


def get_user(db: Session, username: str) -> User:
    stmt = select(User).where(User.username == username)
    try:
        return db.execute(stmt).scalar_one()
    except NoResultFound:
        raise ValueError(f"User with username '{username}' not found.")
    except MultipleResultsFound:
        raise ValueError(f"Multiple users found with username '{username}'.")

def update_user(db: Session, username: str, user_update:UserUpdate):
    try:
        user = get_user(db, username)
        updt = user_update.model_dump(exclude_unset=True)
        for col in updt:
            setattr(user, col, updt[col])
        db.flush()
        db.commit()
        return True
    except:
        db.rollback()
        return False

def delete_user(db: Session, username: str):
    stmt = delete(User).where(User.username == username)
    result = db.execute(stmt)
    db.flush()
    db.commit()
    if result.rowcount > 0:
        return {"message": f"user with '{username}' has been deleted"}
    else:
        raise ValueError(f"User with username '{username}' not found.")
    
'''
Posts CRUD
'''

def get_posts(db: Session):
    stmt = select(Post)
    result = db.execute(stmt)
    return result.scalars().all()

def get_post(db, id: int):
    try:
        stmt = select(Post).where(Post.id == id)
        result = db.execute(stmt)
        return result.scalars().one()
    except NoResultFound:
        raise ValueError(f"Post with '{id}' not found.")

def insert_post(db: Session, post: PostCreate):
    new_post = Post(**post.model_dump(exclude_unset=True))
    db.add(new_post)
    db.flush()
    db.commit()
    return new_post.id

def update_post(db: Session, post_id: int, post_update: PostUpdate):
    try:
        post = get_post(db, post_id)
        updt = post_update.model_dump(exclude_unset=True)
        for col in updt:
            setattr(post, col, updt[col])
        db.flush()
        db.commit()
        return True
    except:
        db.rollback()
        return False
    
def delete_post(db: Session, post_id: int):
    stmt = delete(Post).where(Post.id == post_id)
    result = db.execute(stmt)
    db.flush()
    db.commit()
    if result.rowcount > 0:
        return {"message": f"post with ID: #{post_id} has been deleted"}
    else:
        raise ValueError(f"Post with ID: #{post_id} not found.")
    
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
        raise ValueError(f"Comment with '{id}' not found")

def insert_comment(db: Session, comment: CommentCreate):
    new_comment = Comment(**comment.model_dump(exclude_unset=True))
    db.add(new_comment)
    db.flush()
    db.commit()
    return new_comment.id

def update_comment(db: Session, comment_id: int, comment_update: CommentUpdate):
    try:
        comment = get_comment(db, comment_id)
        updt = comment_update.model_dump(exclude_unset=True)
        for col in updt:
            setattr(comment, col, updt[col])
        db.flush()
        db.commit()
        return True
    except:
        db.rollback()
        return False
    
def delete_comment(db: Session, comment_id: int):
    stmt = delete(Comment).where(Comment.id == comment_id)
    result = db.execute(stmt)
    db.flush()
    db.commit()
    if result.rowcount > 0:
        return {"message": f"comment with ID: #{comment_id} has been deleted"}
    else:
        raise ValueError(f"comment with ID: #{comment_id} not found.")
    
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
        raise ValueError(f"Category with '{id}' not found")
def insert_category(db: Session, category: CategoryCreate):
    new_category = Category(**category.model_dump(exclude_unset=True))
    db.add(new_category)
    db.flush()
    db.commit()
    return new_category.id
def update_category(db: Session, category_id: int, category_update: CategoryUpdate):
    try:
        category = get_category(db, category_id)
        updt = category_update.model_dump(exclude_unset=True)
        for col in updt:
            setattr(category, col, updt[col])
        db.flush()
        db.commit()
        return True
    except NoResultFound: # Catch specific exception
        db.rollback()
        raise ValueError(f"Category with ID '{category_id}' not found.")
    except Exception as e: # Catch other potential errors
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update category: {e}")
def delete_category(db: Session, category_id: int):
    stmt = delete(Category).where(Category.id == category_id)
    result = db.execute(stmt)
    db.flush()
    db.commit()
    if result.rowcount > 0:
        return {"message": f"category with ID: #{category_id} has been deleted"}
    else:
        raise ValueError(f"category with ID: #{category_id} not found.")
    
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
        raise ValueError(f"Tag with '{id}' not found")
def insert_tag(db: Session, tag: TagCreate):
    new_tag = Tag(**tag.model_dump(exclude_unset=True))
    db.add(new_tag)
    db.flush()
    db.commit()
    return new_tag.id
def update_tag(db: Session, tag_id: int, tag_update: TagUpdate):
    try:
        tag = get_tag(db, tag_id)
        updt = tag_update.model_dump(exclude_unset=True)
        for col in updt:
            setattr(tag, col, updt[col])
        db.flush()
        db.commit()
        return True
    except NoResultFound: # Catch specific exception
        db.rollback()
        raise ValueError(f"Tag with ID '{tag_id}' not found.")
    except Exception as e: # Catch other potential errors
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update tag: {e}")
def delete_tag(db: Session, tag_id: int):
    stmt = delete(Tag).where(Tag.id == tag_id)
    result = db.execute(stmt)
    db.flush()
    db.commit()
    if result.rowcount > 0:
        return {"message": f"tag with ID: #{tag_id} has been deleted"}
    else:
        raise ValueError(f"tag with ID: #{tag_id} not found.")