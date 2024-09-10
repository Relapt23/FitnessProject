import jwt
from models import User
from main import users, con
from main import HTTPException, users, User 

SECRET_KEY = 'qwerty'
ALGORITHM = "HS256"

def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # декодируем токен
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
print(token)

username = get_user_from_token(token)

current_user = get_user(username)
