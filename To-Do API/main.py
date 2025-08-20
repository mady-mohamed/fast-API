import fastapi
from fastapi import FastAPI, Query, Security, Depends
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from fastapi import HTTPException
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from datetime import date, datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
from dotenv import load_dotenv
import db
from enum import Enum
'''
Upgrades
1. Async functions
'''

load_dotenv()  # This loads variables from .env file into os.environ

env_vars = {
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "ALGORITHM": os.getenv("ALGORITHM"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
}

'''
FastAPI App
'''
app = FastAPI()


'''
Password Authentication Logic
'''

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() +  (expires_delta or timedelta(minutes= env_vars['ACCESS_TOKEN_EXPIRE_MINUTES']))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, env_vars['SECRET_KEY'], algorithm=env_vars['ALGORITHM'])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        print("Error - hash is unrecognizable: UnknownHashError")
        return False
    except Exception as e:
        # Optional: Log other potential errors from passlib for debugging
        print(f"An unexpected error occurred during password verification: {e}")
        return False

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_q: str = Query(None, alias="token")
):
    token = token_q or token  # prefer query token if provided
    try:
        payload = jwt.decode(token, env_vars['SECRET_KEY'], algorithms=[env_vars['ALGORITHM']])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"username": username, "role": payload.get("role")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def require_role(role: str):
    def role_checker(current_user: dict = fastapi.Depends(get_current_user)):
        if current_user["role"] != role:
            raise HTTPException(status_code=403, detail=f"{role}s only")
        return current_user
    return role_checker

# def create_query_token

@app.get("/protected")
def protected_route(current_user: str = fastapi.Depends(require_role("admin"))):
    return {"message": f"Hello, {current_user['username']}. You are authorized!"}

@app.get("/admin_only")
def admin_only_role(user = fastapi.Depends(require_role("admin"))):
    return {"message": f"Welcome Admin {user['username']}"}

'''
User creation and validation
'''

class User(BaseModel):
    username: str
    password: str
    role: Optional[str] = 'user'

@app.get("/db_users")
def db_users(current_user: dict = fastapi.Depends(require_role("admin"))):
    return db.get_users()

@app.get("/user")
def db_user(id: int, current_user: dict = fastapi.Depends(require_role("admin"))):
    result = db.get_users(id)
    return result


@app.post("/register")
def registration(user: User):
    db.insert_user(user.username, hash_password(user.password), role=user.role)
    return {"message": "User created"}


@app.post("/login")
def login(requests_form = Depends(OAuth2PasswordRequestForm)):
    # Access Pydantic model attributes using dot notation
    user_info = db.get_users(name=str(requests_form.username))

    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Access Pydantic model attributes using dot notation
    if verify_password(requests_form.password, user_info['password']):
        # Use user.username for creating the token
        token = create_access_token({"sub": str(requests_form.username), "role": user_info['role']})
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid username or password")

class UserProfile(BaseModel):
    username: str
    role: str

@app.get("/me", response_model=UserProfile)
def get_user_role(current_user: dict = fastapi.Depends(get_current_user)):
    return current_user

class UserUpdate(BaseModel):
    role: str = None
    name: str = None
    password: str = None

@app.put("/users/{user_id}", dependencies=[Depends(require_role("admin"))])
def update_user(user_id:int, user_update: UserUpdate):
    try:
        cont = {}
        if user_update.role is not None:
            cont["role"] = user_update.role
        if user_update.name is not None:
            cont["name"] = user_update.name
        if user_update.password is not None:
            cont["password"] = hash_password(user_update.password)

        updated = db.update_user(user_id, cont)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User updated"}
    except:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", dependencies=[Depends(require_role("admin"))])
def delete_user(user_id: int):
    if not db.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

'''
Creating, Reading, Updating, and Deleting tasks
'''

class TaskProgress(str, Enum):
    todo = "todo"
    in_progress = "in-progress"
    done = "done"

class Task(BaseModel):
    task_id: Optional[int] = None
    name: str
    progress: TaskProgress
    sprint: int
    start_date: Optional[datetime] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, current_user: dict = fastapi.Depends(get_current_user)):
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/tasks", response_model=List[Task])
def get_tasks(name: str = None, sprint: Optional[int] = None, progress: Optional[str] = None):
    result = db.get_tasks(name, sprint, progress)
    tasks = [
        {
            "task_id": r.id,
            "name": r.name,
            "progress": r.progress,
            "sprint": r.sprint,
            "start_date": r.start_date
        }
        for r in result
    ]
    return tasks

@app.post('/tasks', dependencies=[fastapi.Depends(require_role("admin"))])
def post_task(task: Task):
    start_date = task.start_date
    if task.start_date is None:
        start_date = datetime.utcnow()
    db.insert_task(task.name, task.progress, task.sprint, start_date)
    return {"message": "Task created"}

@app.put("/tasks/{task_id}", response_model=Task, dependencies=[fastapi.Depends(require_role("admin"))])
def update_task(task_id: int, task_update: Task):
    try:
        updated = db.update_task(task_id, task_update.name, task_update.progress, task_update.sprint)
        if not updated: raise HTTPException(status_code=404, detail="Task not found")
        return {  # echo back the update
            "task_id": task_id,
            "name": task_update.name,
            "progress": task_update.progress,
            "sprint": task_update.sprint,
            "start_date": task_update.start_date
        }
    except:
        raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", dependencies=[fastapi.Depends(require_role("admin"))])
def delete_task(task_id: int):
    try:
        db.delete_task(task_id)
    except:
        raise HTTPException(status_code=404, detail="Task not found")