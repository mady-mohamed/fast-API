from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PostUpdate, PostCreate, PostResponse, PostStatus
from schemas import UserCreate,  UserUpdate, UserResponse
from schemas import CommentCreate, CommentUpdate, CommentResponse
from schemas import CategoryUpdate, CategoryCreate, CategoryResponse
from schemas import TagUpdate, TagCreate, TagResponse
from schemas import Token
from models import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from slugify import slugify
from typing import Optional
from crud import get_users, get_user, insert_user, update_user, delete_user
from crud import get_post, get_posts, insert_post, update_post, delete_post
from crud import get_comments, get_comment, insert_comment, update_comment, delete_comment
from crud import get_categories, get_category, insert_category, update_category, delete_category
from crud import get_tags, get_tag, insert_tag, update_tag, delete_tag
from auth import verify_password, create_access_token, hash_password, get_current_user, require_admin


from database import get_db

app = FastAPI(title="Blog API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Blog API"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": user.username, "role": "admin" if user.is_admin else "user"}
    )
    return {"access_token": access_token, "token_type": "bearer"}

'''
Users Endpoints
'''

@app.post("/users/", response_model=UserResponse, tags=["Users"], summary="Create a new user")
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    user_dict = user.model_dump(exclude_unset=True)
    user_dict["password_hash"] = hash_password(user_dict.pop("password"))  # hash before saving
    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{username}", response_model=UserResponse, tags=["Users"], summary="Get a user by username")
def get_single_user(username: str, db: Session = Depends(get_db)):
    return get_user(db, username)
@app.put("/users/{username}", response_model=UserResponse, tags=["Users"], summary="Change user data")
def change_user_data(username: str, update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    user_to_update = get_user(db, username)
    if user_to_update.id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    new_user = update_user(db, username, update)
    db.commit()
    return new_user
@app.delete("/users/{username}", response_model=UserResponse, tags=["Users"], summary="Delete a user by username")
def remove_user(username: str, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    deleted_user = delete_user(db, username)
    db.commit()
    return deleted_user
@app.get("/users/", response_model=list[UserResponse], tags=["Users"], summary="List all registered users")
def list_users(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    return get_users(db)
@app.get("/me", response_model=UserResponse, tags=["Users"], summary="Show current logged in user")
def get_user_role(current_user: dict = Depends(get_current_user)):
    return current_user
'''
Posts Endpoints
'''
@app.post("/posts/", response_model=PostResponse, tags=["Posts"], summary="Create a new post")
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post.author_id = current_user.id
    new_post = insert_post(db, post)
    original_slug = post.slug if post.slug else slugify(post.title)
    unique_slug = f"{original_slug}-{new_post.id}"
    update_data = PostUpdate(slug=unique_slug)
    updated_post = update_post(db, new_post.id, update_data)
    db.commit()
    db.refresh(new_post)
    return updated_post

@app.get("/posts/{post_id}", response_model=PostResponse, tags=["Posts"], summary="Get a single post by post ID")
def get_single_post(post_id: int, db: Session = Depends(get_db)):
    return get_post(db, post_id)
@app.put("/posts/{post_id}", response_model=PostResponse)
def change_post_data(post_id: int, update: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post_to_update = get_post(db, post_id)
    if post_to_update.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    updated_post = update_post(db, post_id, update)
    db.commit()
    return updated_post
@app.delete("/posts/{post_id}", response_model=PostResponse)
def remove_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post_to_delete = get_post(db, post_id)
    if post_to_delete.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    deleted_post = delete_post(db, post_id)
    db.commit()
    return deleted_post
@app.get("/posts/", response_model=list[PostResponse])
def list_posts(
    skip: int = 0, 
    limit: int = 10, 
    status: Optional[PostStatus] = None, # New optional filter
    db: Session = Depends(get_db)
):
    # Pass the new status parameter to the CRUD function
    return get_posts(db, skip=skip, limit=limit, status=status)
'''
Comments Endpoints
'''
@app.post("/comments/", response_model=CommentResponse)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment.author_id = current_user.id
    new_comment = insert_comment(db, comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
@app.get("/comments/{comment_id}", response_model=CommentResponse)
def get_single_comment(comment_id: int, db: Session = Depends(get_db)):
    return get_comment(db, comment_id)
@app.put("/comments/{comment_id}", response_model=CommentResponse)
def change_comment_data(comment_id: int, update: CommentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment_to_update = get_comment(db, comment_id)
    if comment_to_update.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    updated_comment = update_comment(db, comment_id, update)
    db.commit()
    return updated_comment
@app.delete("/comments/{comment_id}", response_model=CommentResponse)
def remove_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment_to_delete = get_comment(db, comment_id)
    if comment_to_delete.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    deleted_comment = delete_comment(db, comment_id)
    db.commit()
    return deleted_comment
@app.get("/comments/", response_model=list[CommentResponse])
def list_comments(db: Session = Depends(get_db)):
    return get_comments(db)
'''
Categories Endpoints
'''
@app.post("/categories/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = insert_category(db, category)
    original_slug = category.slug if category.slug else slugify(category.name)
    unique_slug = f"{original_slug}-{new_category.id}"
    update_data = CategoryUpdate(slug=unique_slug)
    update_category(db, new_category.id, update_data)
    db.commit()
    db.refresh(new_category)
    return new_category
@app.get("/categories/{category_id}", response_model=CategoryResponse)
def get_single_category(category_id: int, db: Session = Depends(get_db)):
    return get_category(db, category_id)
@app.put("/categories/{category_id}")
def change_category_data(category_id: int, update: CategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    updated_category = update_category(db, category_id, update)
    db.commit()
    return updated_category
@app.delete("/categories/{category_id}", response_model=CategoryResponse)
def remove_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    deleted_category = delete_category(db, category_id)
    db.commit()
    return deleted_category
@app.get("/categories/", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)
'''
Tags Endpoints
'''
@app.post("/tags/", response_model=TagResponse)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    new_tag = insert_tag(db, tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag
@app.get("/tags/{tag_id}", response_model=TagResponse)
def get_single_tag(tag_id: int, db: Session = Depends(get_db)):
    return get_tag(db, tag_id)
@app.put("/tags/{tag_id}", response_model=TagResponse)
def change_tag_data(tag_id: int, update: TagUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    updated_tag = update_tag(db, tag_id, update)
    db.commit()
    return updated_tag
@app.delete("/tags/{tag_id}", response_model=TagResponse)
def remove_tag(tag_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    tag = delete_tag(db, tag_id)
    db.commit()
    return tag
@app.get("/tags/", response_model=list[TagResponse])
def list_tags(db: Session = Depends(get_db)):
    return get_tags(db)