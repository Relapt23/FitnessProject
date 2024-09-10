from pydantic import BaseModel



class User(BaseModel):
    username: str
    password: str


class Params(BaseModel):
    type: str
    intensity: str

