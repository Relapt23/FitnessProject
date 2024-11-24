from fastapi import FastAPI, Depends, Request, Query
from models import Base, User, Users, ChooseExercises, Exercises, UserRequest, CombinationsMusclesTypes, Workouts
from sqlalchemy import MetaData, create_engine, select, insert
from sqlalchemy.orm import sessionmaker, Session
from security import create_jwt_token
import random
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
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

@app.get("/combinations/intensity/workouts/{id}", response_class=HTMLResponse)
async def enter_combination(request: Request, id: int):
    workouts = get_workouts(id)
    return templates.TemplateResponse(name="user_workouts.html", context={"request":request, "workouts": workouts}) 
def get_workouts(combination_id: int):
    random_training_number = random.randint(1,3)
    ans = []
    with sess() as session:
        query = select(Workouts)
        res = session.execute(query)
        training_list = res.scalars().all()
        for ex in training_list:
            if combination_id == ex.combination_id and random_training_number == ex.training_number:
                ans.append({"title": ex.exercise, "per": ex.periodicity})
        session.commit()
    return ans

@app.get("/combinations/", response_class=HTMLResponse)
async def choose_combination(request: Request):
    combinations_list = []
    array = []
    with sess() as session:
        query = select(CombinationsMusclesTypes)
        res = session.execute(query)
        combinations = res.scalars().all()
        for combination in combinations:
            array.append({"title":combination.title, "id": combination.id})
        for dict in array:
            i = return_index(dict["title"], combinations_list)
            if i == None:
                combinations_list.append({"title": dict["title"], "ids": [dict["id"]]})
            else:
                combinations_list[i]["ids"].append(dict["id"])
    return templates.TemplateResponse(name="combinations.html", context={"request":request, "training": combinations_list}) 
def return_index(title, combinations_list):
    for i, elem in enumerate(combinations_list):
        if title == elem["title"]:
            return i
    return None
    


@app.get("/combinations/intensity/", response_class=HTMLResponse)
async def choose_intensity(request: Request, id: List[int] = Query([])):
    ans = []
    with sess() as session:
        query = select(CombinationsMusclesTypes)
        res = session.execute(query)
        combinations = res.scalars().all()
        for combination in combinations:
            if combination.id in id:
                if combination.intensity == 1:
                    ans.append({"id": combination.id, "title": combination.title, "intensity": "Легкая"})
                elif combination.intensity == 2:
                    ans.append({"id": combination.id, "title": combination.title, "intensity": "Средняя"})
                else:
                    ans.append({"id": combination.id, "title": combination.title, "intensity": "Тяжелая"})
    
    return templates.TemplateResponse(name="intensity.html", context={"request":request, "intensity": ans})

@app.get("/auto", response_class=HTMLResponse)
def auto(request: Request):
    return templates.TemplateResponse(name="auto.html", context={"request":request, "intensity": 4})

@app.get("/login55", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})