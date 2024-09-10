from fastapi import FastAPI, HTTPException
from models import User
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine

app = FastAPI()

metadata = MetaData()
engine = create_engine("sqlite:///database.db")
users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String),
    Column('password', String),
    Column('exceptions', String)
)

exercises = Table(
    'exercises', metadata,
    Column('id', Integer, primary_key=True),
    Column('type', String),
    Column('title', String)
)

muscle_types = Table(
    'muscle_types', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String)
)

intensity = Table(
    'intensity', metadata,
    Column('id', Integer, primary_key=True),
    Column('intensity', String)
)

exercises_preset = Table(
    'exercises_preset', metadata,
    Column('exercises_id', Integer, primary_key=True),
    Column('intensity', String),
    Column('periodicity', String)
)

exceptions = Table(
    'exceptions', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('exercises_id', Integer),
)

metadata.create_all(engine)
con = engine.connect()

# def get_user(user: User):
#     s = users.select()
#     rows = con.execute(s).fetchall()
#     con.commit()
#     for elem in rows:
#         if elem[1] == user.username:
#             raise HTTPException(status_code=418, detail="User in database")
#     con.execute(users.insert().values(username=user.username, password=user.password))
#     con.commit()
#     return {"message":"Successful registration", "user": user.username}