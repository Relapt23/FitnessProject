# from fastapi import FastAPI, HTTPException
# from models import User, Users
# from main import app, users, con, sess, select, insert
# from security import create_jwt_token, Depends, get_user_from_token, get_user

# @app.post('/login')
# async def login_user(user: User):
#     print("ewfew")
#     with sess() as session:
#         query = select(Users)
#         res = session.execute(query)
#         users = res.scalars().all()
#         print(users)
#         for person in users:
#             print(person)
#         if user.username not in users:
#             session.execute(insert(Users), {"username": user.username, "password": user.password})
#             session.commit()
#         return {"message": "Successful registration"}
#     #         if person[1] == user.username and person[2] == user.password:
#     #             return {"access_token": create_jwt_token({"sub": user.username}), "token_type": "bearer"}
#     # if user.username not in users:
#     #     con.execute(users.insert().values(username=user.username, password=user.password))
#     #     con.commit()
#     #     return {"message": "Successful registration"}
#     # else:
#     #     return {"error": "User in database"}

# @app.get("/about_me")
# async def user_info(current_user: str = Depends(get_user_from_token)):
#     user = get_user(current_user)
#     print(user)
#     if user:
#         return user
#     return {"Error": "User not found"}
