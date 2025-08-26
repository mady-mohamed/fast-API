import sqlalchemy as sa
import glob
from datetime import datetime
from fastapi import Query
from sqlalchemy.ext.asyncio import create_async_engine
import sqlalchemy.ext.asyncio as ay
import asyncio

# Database Implementation

db_file = "test.db"
db_path = glob.glob(f"*{db_file}")

DATABASE_URL = f"sqlite:///./{db_file}"
db_async_url = f"sqlite+aiosqlite:///./{db_file}"

metadata = sa.MetaData()

user_table = sa.Table(
    "user",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String),
    sa.Column("password", sa.String),
    sa.Column("role", sa.String)
)

task_table = sa.Table(
    "task",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String),
    sa.Column("progress", sa.String),
    sa.Column("sprint", sa.INTEGER),
    sa.Column("start_date", sa.DATETIME)
)

engine = None

async def create_tables(db_url: str, db_path):
    global engine
    engine = create_async_engine(db_url, echo=True)
    if len(db_path) < 1:
        async with engine.begin() as conn:
            await conn.run_sync(metadata.create_all)
    return engine

'''
User Logic
'''

async def insert_user(name: str, password:str, role:str = "user"):
    async with engine.begin() as conn:
        await conn.execute(sa.insert(user_table).values(name = name, password = password, role = role))

async def get_users(id: int = None, name: str = None):
    async with engine.connect() as conn:
        stmt = sa.select(user_table)
        if name is not None:
            stmt = stmt.where(user_table.c.name == name)
        elif id is not None:
            stmt = stmt.where(user_table.c.id == id)
        result = await conn.execute(stmt)
        if id or name:
            row = result.first()
            return row._asdict() if row else None
        else:
            return [u._asdict() for u in result]

async def update_user(id: int, cont: dict) -> bool:
    async with engine.begin() as conn:
        result = await conn.execute(
            sa.update(user_table).where(user_table.c.id == id).values(cont)
        )
        return result.rowcount > 0   # True if any row updated

async def delete_user(id: int) -> bool:
    async with engine.begin() as conn:
        result = await conn.execute(sa.delete(user_table).where(user_table.c.id == id))
        return result.rowcount > 0


'''
Task Logic
'''

async def get_task(task_id: int):
    async with engine.connect() as conn:
        stmt = sa.select(task_table).where(task_table.c.id == task_id)
        result = await conn.execute(stmt).first()
        return result._asdict() if result else None
    

async def insert_task(name: str, progress:str, sprint: int, date: datetime):
    async with engine.begin() as conn:
        await conn.execute(sa.insert(task_table).values(name = name, progress = progress, sprint = sprint, start_date = date))

async def get_tasks(name: str = None, sprint: int = None, progress: str = None):
    async with engine.connect() as conn:
        stmt = sa.select(task_table)
        conditions = []
        if name is not None:
            conditions.append(task_table.c.name == name)
        if progress is not None:
            conditions.append(task_table.c.progress == progress)
        if sprint is not None:
            conditions.append(task_table.c.sprint == sprint)
        if conditions:
            stmt = stmt.where(sa.and_(*conditions))
        result = await conn.execute(stmt)
        return result.all()

async def update_task(id: int, name: str = None, progress: str = None, sprint: int = None):
    async with engine.begin() as conn:
        cont = {}
        if name is not None:
            cont['name'] = name
        if progress is not None:
            cont["progress"] = progress
        if sprint is not None:
            cont["sprint"] = sprint
        res = await conn.execute(sa.update(task_table).where(task_table.c.id == id).values(cont))
        return res.rowcount > 0

async def delete_task(id: int):
    async with engine.begin() as conn:
        res = await conn.execute(sa.delete(task_table).where(task_table.c.id == id))
        return res.rowcount > 0