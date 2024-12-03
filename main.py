from fastapi import FastAPI, Depends, Request, Query
from models import Base, User, Users, ChooseExercises, Exercises, UserRequest, CombinationsMusclesTypes, Workouts
from sqlalchemy import MetaData, create_engine, select, insert
from sqlalchemy.orm import sessionmaker, Session
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

@app.get("/combinations/intensity/workouts/{id}", response_class=HTMLResponse)
async def enter_combination(request: Request, id: int):
    workouts = get_workouts(id)
    return templates.TemplateResponse(name="user_workouts.html", context={"request":request, "workouts": workouts}) 
def get_workouts(combination_id: int):
    random_training_number = random.randint(1,3)
    array = []
    ans = []
    with sess() as session:
        query = select(Workouts)
        res = session.execute(query)
        training_list = res.scalars().all()
        for ex in training_list:
            if combination_id == ex.combination_id and random_training_number == ex.training_number:
                array.append({"title": ex.exercise, "per": ex.periodicity})
        query2 = select(Exercises)
        res2 = session.execute(query2)
        exercises_list = res2.scalars().all()
        for exercise in exercises_list:
            for elem in array:
                if elem["title"] == exercise.title and exercise.youtube not in ans:
                    ans.append({"title": elem["title"], "per": elem["per"], "youtube": exercise.youtube})
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

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})