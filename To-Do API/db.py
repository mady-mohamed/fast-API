import sqlalchemy as sa
import glob
from datetime import datetime

db_file = "test.db"
db_path = glob.glob(f"*{db_file}")

DATABASE_URL = f"sqlite:///./{db_file}"

engine = sa.create_engine(DATABASE_URL)

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

if len(db_path) < 1:
    metadata.create_all(engine)

'''
User Logic
'''

def insert_user(name: str, password:str, role:str = "user"):
    connection = None
    try:
        connection = engine.connect()
        connection.execute(sa.insert(user_table).values(name = name, password = password, role = role))
        connection.commit()
    finally:
        if connection:
            connection.close()

def get_users(name: str = None):
    connection = None
    try:
        connection = engine.connect()
        stmt = sa.select(user_table)
        if name is not None:
            stmt = stmt.where(user_table.c.name == name)
        result = connection.execute(stmt)
        users = result.all()
        return users
    finally:
        if connection:
            connection.close()


def update_user(name: str, password: str = None, role: str = None):
    connection = None
    try:
        connection = engine.connect()

        # Build the dictionary of values to be updated
        cont = {}
        if password is not None:
            cont['password'] = password
        if role is not None:
            cont['role'] = role

        # Create a single UPDATE statement and execute it
        connection.execute(sa.update(user_table).where(user_table.c.name == name).values(cont))
        connection.commit()

    finally:
        if connection:
            connection.close()

def delete_user(name:str):
    connection = None
    try:
        connection = engine.connect()
        connection.execute(sa.delete(user_table).where(user_table.c.name == name))
        connection.commit()
    finally:
        if connection:
            connection.close()

'''
Task Logic
'''

def insert_task(name: str, progress:str, sprint: int, date: datetime):
    connection = None
    try:
        connection = engine.connect()
        connection.execute(sa.insert(task_table).values(name = name, progress = progress, sprint = sprint, start_date = date))
        connection.commit()
    finally:
        if connection:
            connection.close()

def get_tasks(name: str = None, sprint: int = None, progress: str = None):
    connection = None
    try:
        connection = engine.connect()
        stmt = sa.select(task_table)
        conditions = []
        if name is not None:
            conditions.append(task_table.c.name == name)
        if progress is not None:
            conditions.append(task_table.c.progress == progress)
        if sprint is not None:
            conditions.append(task_table.c.sprint == sprint)
        stmt = stmt.where(sa.and_(*conditions))
        result = connection.execute(stmt)
        tasks = result.all()
        return tasks
    finally:
        if connection:
            connection.close()
def update_task(id: int, name: str = None, progress: str = None, sprint: int = None):
    connection = None
    try:
        connection = engine.connect()
        cont = {}
        if name is not None:
            cont['name'] = name
        if progress is not None:
            cont["progress"] = progress
        if sprint is not None:
            cont["sprint"] = sprint
        connection.execute(sa.update(task_table).where(task_table.c.id == id).values(cont))
        connection.commit()
    finally:
        if connection:
            connection.close()
def delete_task(id: int):
    connection = None
    try:
        connection = engine.connect()
        connection.execute(sa.delete(task_table).where(task_table.c.id == id))
        connection.commit()
    finally:
        if connection:
            connection.close()