from models import User, Post
from sqlalchemy import select, delete
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from schemas import UserCreate, UserUpdate, PostCreate, PostUpdate
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

def get_user(db: Session, username: str):
    try:
        stmt = select(User).where(User.username == username)
        result = db.execute(stmt)
        return result.scalars().one()
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

def insert_post(db: Session, post: PostCreate):
    new_post = Post(**post.model_dump(exclude_unset=True))
    db.add(new_post)
    db.flush()
    db.commit()
    return new_post.id

def get_post(db, id: int):
    try:
        stmt = select(Post).where(Post.id == id)
        result = db.execute(stmt)
        return result.scalars().one()
    except NoResultFound:
        raise ValueError(f"Post with '{id}' not found.")

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
    