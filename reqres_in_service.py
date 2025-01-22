from typing import List
from fastapi import FastAPI, HTTPException

from auth_db import auth_db
from json_loader import load_json
from model.auth import LoginResponse, AuthData
from model.user import UserData


app = FastAPI()
users = {}

@app.post("/api/login")
def login(auth: AuthData, response_model=LoginResponse):
    if auth.email in auth_db and auth.password == auth_db[auth.email]:
        return LoginResponse(token="QpwL5tke4Pnpja7X4")
    else:
        raise HTTPException(status_code=400, detail="неверный логин или пароль")


@app.get("/api/users", response_model=List[UserData])
def get_users():
    return users.values()


@app.get("/api/users/{user_id}", response_model=UserData)
def get_user(user_id: int):
    if user_id in users:
        return users[user_id]
    else:
        raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    import uvicorn
    users = load_json("users.json")

    uvicorn.run(app, host="127.0.0.1", port=8080)
