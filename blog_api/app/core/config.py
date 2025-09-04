import os
from dotenv import load_dotenv

load_dotenv()  # load variables from .env

class Settings:
    PROJECT_NAME: str = "Blog API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./blog.db")

settings = Settings()