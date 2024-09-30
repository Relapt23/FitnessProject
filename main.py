from fastapi import FastAPI
from models import Base
from sqlalchemy import MetaData, create_engine, select
from sqlalchemy.orm import sessionmaker, Session



app = FastAPI()
metadata = MetaData()
engine = create_engine("sqlite:///database.db",echo=True)
sess = sessionmaker(engine)

def create_tables():
    engine.echo = False
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    engine.echo = True

def insert_data():
    with sess() as session:
        raw_connection = session.get_bind().raw_connection()
        raw_cursor = raw_connection.cursor()
        raw_cursor.executescript(open("initial_data.sql").read())
        session.commit()
        
create_tables()
insert_data()
# with sess() as session:
#     query = select(Exercises)
#     res = session.execute(query)
#     exercises = res.scalars().all()
#     print(f"{exercises=}")
#     for elem in exercises:
#         print(elem.title, elem.type)

