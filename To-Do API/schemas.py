from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class User(BaseModel):
    username: str
    password: str
    role: Optional[str] = 'user'
    
class UserProfile(BaseModel):
    username: str
    role: str
    
class UserUpdate(BaseModel):
    role: str = None
    name: str = None
    password: str = None
    
    
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
    