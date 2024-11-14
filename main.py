from fastapi import FastAPI, Depends
from models import Base, User, Users, ChooseExercises, Exercises, UserRequest, CombinationsMusclesTypes, Workouts
from sqlalchemy import MetaData, create_engine, select, insert
from sqlalchemy.orm import sessionmaker, Session
from security import create_jwt_token
import random


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

@app.put("/{user}/")
async def enter_combination(user: str, request: UserRequest):
    id_combination = 0
    intensity_combination = 0
    random_training_number = random.randint(1,3)
    user_intensity = 0
    ans = []
    if request.intensity == "Легкая":
        user_intensity = 1
    elif request.intensity == "Средняя":
        user_intensity = 2
    else:
        user_intensity = 3
    with sess() as session:
        query = select(CombinationsMusclesTypes)
        res = session.execute(query)
        combinations = res.scalars().all()
        for combination in combinations:
            if  request.combination == combination.title and combination.intensity == user_intensity:
                id_combination = combination.id
                intensity_combination = combination.intensity
                break
        query = select(Workouts)
        res = session.execute(query)
        training_list = res.scalars().all()
        for ex in training_list:
            if id_combination == ex.combination_id and intensity_combination == ex.intensity and random_training_number == ex.training_number:
                ans.append({"title": ex.exercise, "per": ex.periodicity})
        print(ans)
        session.commit()
    return ans
