import fastapi, glob
from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from fastapi import HTTPException
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
import db
from enum import Enum
from password import *
from schemas import *

load_dotenv()  # This loads variables from .env file into os.environ

db_file = "test.db"

db_async_url = f"sqlite+aiosqlite:///./{db_file}"
db_path = glob.glob(f"*{db_file}")

'''
FastAPI App
'''
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await db.create_tables(db_async_url, db_path)

'''
Password Authentication Logic
'''
# The route handlers also need to be async now
@app.get("/protected")
async def protected_route(current_user: str = fastapi.Depends(require_role("admin"))):
    return {"message": f"Hello, {current_user['username']}. You are authorized!"}

@app.get("/admin_only")
async def admin_only_role(user = fastapi.Depends(require_role("admin"))):
    return {"message": f"Welcome Admin {user['username']}"}

'''
User creation and validation
'''

class User(BaseModel):
    username: str
    password: str
    role: Optional[str] = 'user'

# This route calls an async function
@app.get("/db_users")
async def db_users(current_user: dict = fastapi.Depends(require_role("admin"))):
    return await db.get_users()

# This route calls an async function
@app.get("/user")
async def db_user(id: int, current_user: dict = fastapi.Depends(require_role("admin"))):
    result = await db.get_users(id)
    return result

# This route calls an async function
@app.post("/register")
async def registration(user: User):
    await db.insert_user(user.username, hash_password(user.password), role=user.role)
    return {"message": "User created"}


# This route calls an async function
@app.post("/login")
async def login(requests_form = Depends(OAuth2PasswordRequestForm)):
    user_info = await db.get_users(name=str(requests_form.username))

    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if verify_password(requests_form.password, user_info['password']):
        token = create_access_token({"sub": str(requests_form.username), "role": user_info['role']})
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid username or password")

class UserProfile(BaseModel):
    username: str
    role: str

@app.get("/me", response_model=UserProfile)
async def get_user_role(current_user: dict = fastapi.Depends(get_current_user)):
    return current_user

class UserUpdate(BaseModel):
    role: str = None
    name: str = None
    password: str = None

# This route calls an async function
@app.put("/users/{user_id}", dependencies=[Depends(require_role("admin"))])
async def update_user(user_id:int, user_update: UserUpdate):
    try:
        cont = {}
        if user_update.role is not None:
            cont["role"] = user_update.role
        if user_update.name is not None:
            cont["name"] = user_update.name
        if user_update.password is not None:
            cont["password"] = hash_password(user_update.password)

        updated = await db.update_user(user_id, cont)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User updated"}
    except:
        raise HTTPException(status_code=404, detail="User not found")

# This route calls an async function
@app.delete("/users/{user_id}", dependencies=[Depends(require_role("admin"))])
async def delete_user(user_id: int):
    if not await db.delete_user(user_id):
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

# This route calls an async function
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, current_user: dict = fastapi.Depends(get_current_user)):
    task = await db.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# This route calls an async function
@app.get("/tasks", response_model=List[Task])
async def get_tasks(name: str = None, sprint: Optional[int] = None, progress: Optional[str] = None):
    result = await db.get_tasks(name, sprint, progress)
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

# This route calls an async function
@app.post('/tasks', dependencies=[fastapi.Depends(require_role("admin"))])
async def post_task(task: Task):
    start_date = task.start_date
    if task.start_date is None:
        start_date = datetime.utcnow()
    await db.insert_task(task.name, task.progress, task.sprint, start_date)
    return {"message": "Task created"}

# This route calls an async function
@app.put("/tasks/{task_id}", response_model=Task, dependencies=[fastapi.Depends(require_role("admin"))])
async def update_task(task_id: int, task_update: Task):
    try:
        updated = await db.update_task(task_id, task_update.name, task_update.progress, task_update.sprint)
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

# This route calls an async function
@app.delete("/tasks/{task_id}", dependencies=[fastapi.Depends(require_role("admin"))])
async def delete_task(task_id: int):
    try:
        await db.delete_task(task_id)
    except:
        raise HTTPException(status_code=404, detail="Task not found")
