import sqlalchemy as sa
import glob

db_file = "test.db"
db_path = glob.glob(f"*{db_file}")

DATABASE_URL = f"sqlite:///./{db_file}"

engine = sa.create_engine(DATABASE_URL)
connection = engine.connect()

metadata = sa.MetaData()

user_table = sa.Table(
    "user",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String),
    sa.Column("password", sa.String),
    sa.Column("role", sa.String)
)

if len(db_path) < 1:
    metadata.create_all(engine)

def insert_user(name: str, password:str, role:str = "user"):
    connection = None
    try:
        connection = engine.connect()
        connection.execute(sa.insert(user_table).values(name = name, password = password, role = role))
        connection.commit()
        connection.close()
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
        connection.close()
    finally:
        if connection:
            connection.close()
