from fastapi import FastAPI, HTTPException
from models import User
from main import app, users, con

@app.post('/')
def login_user(user: User):
