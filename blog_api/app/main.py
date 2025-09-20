from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas import PostUpdate, PostCreate 
from schemas import UserCreate,  UserUpdate
from schemas import CommentCreate, CommentUpdate
from schemas import CategoryUpdate, CategoryCreate
from schemas import TagUpdate, TagCreate
from crud import get_users, get_user, insert_user, update_user, delete_user
from crud import get_post, get_posts, insert_post, update_post, delete_post
from crud import get_comments, get_comment, insert_comment, update_comment, delete_comment
from crud import get_categories, get_category, insert_category, update_category, delete_category
from crud import get_tags, get_tag, insert_tag, update_tag, delete_tag

from database import get_db

app = FastAPI(title="Blog API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Blog API"}
'''
Users Endpoints
'''
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    success_id = insert_user(db, user)
    return {"message": f"User #{success_id} created"}
@app.get("/users/{username}")
def get_single_user(username: str, db: Session = Depends(get_db)):
    return get_user(db, username)
@app.put("/users/{username}")
def change_user_data(username: str, update: UserUpdate, db: Session = Depends(get_db)):
    cond = update_user(db, username, update)
    if cond:
        return {"message": f"{username} has been updated"}
    else:
        return {"message": f"{username} has not been found"}
@app.delete("/users/{username}")
def remove_user(username: str, db: Session = Depends(get_db)):
    return delete_user(db, username)
@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    return get_users(db)
'''
Posts Endpoints
'''
@app.post("/posts/")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    success_id = insert_post(db, post)
    return {"message": f"Post #{success_id} created"}
@app.get("/posts/{post_id}")
def get_single_post(post_id: int, db: Session = Depends(get_db)):
    return get_post(db, post_id)
@app.put("/posts/{post_id}")
def change_post_data(post_id: int, update: PostUpdate, db: Session = Depends(get_db)):
    cond = update_post(db, post_id, update)
    if cond:
        return {"message": f"Post #{post_id} has been updated"}
    else:
        return {"message": f"Post #{post_id} has not been found"}
@app.delete("/posts/{post_id}")
def remove_post(post_id: int, db: Session = Depends(get_db)):
    return delete_post(db, post_id)
@app.get("/posts/")
def list_posts(db: Session = Depends(get_db)):
    return get_posts(db)
'''
Comments Endpoints
'''
@app.post("/comments/")
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    success_id = insert_comment(db, comment)
    return {"message": f"Comment #{success_id} created"}
@app.get("/comments/{comment_id}")
def get_single_comment(comment_id: int, db: Session = Depends(get_db)):
    return get_comment(db, comment_id)
@app.put("/comments/{comment_id}")
def change_comment_data(comment_id: int, update: CommentUpdate, db: Session = Depends(get_db)):
    cond = update_comment(db, comment_id, update)
    if cond:
        return {"message": f"Comment #{comment_id} has been updated"}
    else:
        return {"message": f"Comment #{comment_id} has not been found"}
@app.delete("/comments/{comment_id}")
def remove_comment(comment_id: int, db: Session = Depends(get_db)):
    return delete_comment(db, comment_id)
@app.get("/comments/")
def list_comments(db: Session = Depends(get_db)):
    return get_comments(db)
'''
Categories Endpoints
'''
@app.post("/categories/")
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    success_id = insert_category(db, category)
    return {"message": f"Category #{success_id} created"}
@app.get("/categories/{category_id}")
def get_single_category(category_id: int, db: Session = Depends(get_db)):
    return get_category(db, category_id)
@app.put("/categories/{category_id}")
def change_category_data(category_id: int, update: CategoryUpdate, db: Session = Depends(get_db)):
    cond = update_category(db, category_id, update)
    if cond:
        return {"message": f"Category #{category_id} has been updated"}
    else:
        return {"message": f"Category #{category_id} has not been found"}
@app.delete("/categories/{category_id}")
def remove_category(category_id: int, db: Session = Depends(get_db)):
    return delete_category(db, category_id)
@app.get("/categories/")
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)
'''
Tags Endpoints
'''
@app.post("/tags/")
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    success_id = insert_tag(db, tag)
    return {"message": f"Tag #{success_id} created"}
@app.get("/tags/{tag_id}")
def get_single_tag(tag_id: int, db: Session = Depends(get_db)):
    return get_tag(db, tag_id)
@app.put("/tags/{tag_id}")
def change_tag_data(tag_id: int, update: TagUpdate, db: Session = Depends(get_db)):
    cond = update_tag(db, tag_id, update)
    if cond:
        return {"message": f"Tag #{tag_id} has been updated"}
    else:
        return {"message": f"Tag #{tag_id} has not been found"}
@app.delete("/tags/{tag_id}")
def remove_tag(tag_id: int, db: Session = Depends(get_db)):
    return delete_tag(db, tag_id)
@app.get("/tags/")
def list_tags(db: Session = Depends(get_db)):
    return get_tags(db)