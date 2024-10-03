import jwt
from fastapi.security import OAuth2PasswordBearer
from models import User
# from main import users, con, Depends
# from main import HTTPException, users
from fastapi import HTTPException, Depends

SECRET_KEY = 'qwerty'
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_user(username: str):
    s = users.select()
    rows = con.execute(s).fetchall()
    con.commit()
    for person in rows:
        if person[1] == username:
            return person[1]
    return None

token = create_jwt_token({"sub": "user"})

