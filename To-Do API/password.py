from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Query, Security, Depends, HTTPException
from db import get_users
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

# This function now needs to be async because it calls db.get_users
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_q: str = Query(None, alias="token")
):
    token = token_q or token  # prefer query token if provided
    try:
        payload = jwt.decode(token, env_vars['SECRET_KEY'], algorithms=[env_vars['ALGORITHM']])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # This is now an async call and needs to be awaited
        user = await get_users(name=username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"username": username, "role": payload.get("role")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def require_role(role: str):
    # This inner function needs to be async because its dependency is now async
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != role:
            raise HTTPException(status_code=403, detail=f"{role}s only")
        return current_user
    return role_checker