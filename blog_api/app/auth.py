# auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Query, Security, Depends, HTTPException
from crud import get_user # Keep this import, as get_current_user needs it
from database import get_db
from sqlalchemy.orm import Session
from models import User
from security import verify_password # Import from the new security file


import os

load_dotenv()

print(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
env_vars = {
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "ALGORITHM": os.getenv("ALGORITHM"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
}

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() +  (expires_delta or timedelta(minutes= env_vars['ACCESS_TOKEN_EXPIRE_MINUTES']))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, env_vars['SECRET_KEY'], algorithm=env_vars['ALGORITHM'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_q: str = Query(None, alias="token"),
    db: Session = Depends(get_db)
):
    token = token_q or token
    try:
        payload = jwt.decode(token, env_vars['SECRET_KEY'], algorithms=[env_vars['ALGORITHM']])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user = get_user(db, username) 
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user