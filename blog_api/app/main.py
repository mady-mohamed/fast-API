from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas import PostUpdate, UserCreate, PostCreate, UserUpdate
from crud import get_users, get_user, insert_user, update_user, delete_user
from crud import get_post, get_posts, insert_post, update_post, delete_post
from database import get_db

app = FastAPI(title="Blog API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Blog API"}

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

@app.post("/posts/")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    success_id = insert_post(db, post)
    return {"message": f"Post #{success_id} created"}
@app.get("/posts/{post_id}")
def get_single_post(post_id: int, db: Session = Depends(get_db)):
    return get_post(db, post_id)
@app.put("/posts/{id}")
def change_post_data(post_id: int, update: PostUpdate, db: Session = Depends(get_db)):
    cond = update_post(db, post_id, update)
    if cond:
        return {"message": f"Post #{post_id} has been updated"}
    else:
        return {"message": f"Post #{post_id} has not been found"}
@app.delete("/posts/{id}")
def remove_post(post_id: int, db: Session = Depends(get_db)):
    return delete_post(db, post_id)
@app.get("/posts/")
def list_posts(db: Session = Depends(get_db)):
    return get_posts(db)