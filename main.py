from fastapi import FastAPI, Depends
from models import Base, User, Users, ChooseExercises, Exercises
from sqlalchemy import MetaData, create_engine, select, insert
from sqlalchemy.orm import sessionmaker, Session
from security import create_jwt_token


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

@app.post('/login')
async def login_user(user: User):
    with sess() as session:
        query = select(Users)
        res = session.execute(query)
        users = res.scalars().all()
        for person in users:
            if person.username == user.username and person.password == user.password:
                return {"access_token": create_jwt_token({"sub": user.username}), "token_type": "bearer"}
        session.execute(insert(Users), {"username": user.username, "password": user.password})
                # query = select(Users)
                # res = session.execute(query)
                # users = res.scalars().all()
        session.commit()
        return {"message": "Successful registration"}
    
@app.post("/user")
async def choose_exercises(types_id: ChooseExercises):
    with sess() as session:
        for id in types_id.muscles_types_id:
            stmt = select(Exercises.title).where(Exercises.type == id)
            for row in session.execute(stmt):
                print(row)


# @app.get("/about_me")
# async def user_info(current_user: str = Depends(get_user_from_token)):
#     user = get_user(current_user)
#     print(user)
#     if user:
#         return user
#     return {"Error": "User not found"}

