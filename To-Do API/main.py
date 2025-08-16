import fastapi
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import date, datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
import db

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
    return pwd_context.verify(plain_password, hashed_password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = fastapi.Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, env_vars['SECRET_KEY'], algorithms=env_vars['ALGORITHM'])
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
    result = db.get_users()
    user = [
        {
            "user_id": r.id,
            "username": r.name,
            "password": r.password,
            "role": r.role
        }
        for r in result
    ]
    return user


@app.post("/register")
def registration(user: User):
    db.insert_user(user.username, hash_password(user.password), role=user.role)
    return {"message": "User created"}


@app.post("/login")
def login(user: User):
    existing_user = db.get_users(user.username)
    if len(existing_user) < 1:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    user_password_hashed = existing_user[0][2]
    if verify_password(user.password, user_password_hashed):
        role = existing_user[0][3]
        token = create_access_token({"sub": user.username, "role": role})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")


'''
Creating, Reading, Updating, and Deleting tasks
'''

tasks = [
    {"task_id": 1, "name": "Task 1", "progress": "Finished", "sprint": 1, "start_date": date(2000, 1, 1)},
    {"task_id": 2, "name": "Task 2", "progress": "Working", "sprint": 1, "start_date": date(2000, 1, 1)},
    {"task_id": 3, "name": "Task 3", "progress": "Pending", "sprint": 1, "start_date": date(2000, 1, 1)}
]

class Task(BaseModel):
    task_id: Optional[int] = None
    name: str
    progress: str
    sprint: int
    start_date: date

    model_config = ConfigDict(arbitrary_types_allowed=True)


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
    db.insert_task(task.name, task.progress, task.sprint, task.start_date)
    return {"message": "Task created"}


@app.put("/tasks/{task_id}", response_model=Task, dependencies=[fastapi.Depends(require_role("admin"))])
def update_task(task_id: int, task_update: Task):
    try:
        db.update_task(task_id, task_update.name, task_update.progress, task_update.sprint)
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