import os

import dotenv
from fastapi import FastAPI, HTTPException
from auth_db import auth_db
from json_loader import load_json
from model.app_status import AppStatus
from model.auth import LoginResponse, AuthData
from model.user import UserData
from fastapi_pagination import Page, paginate, add_pagination

app = FastAPI()


users = {}


@app.get("/api/status")
def status() -> AppStatus:
    return AppStatus(users=bool(users))


@app.post("/api/login")
def login(auth: AuthData) -> LoginResponse:
    if auth.email in auth_db and auth.password == auth_db[auth.email]:
        return LoginResponse(token="QpwL5tke4Pnpja7X4")
    else:
        raise HTTPException(status_code=400, detail="неверный логин или пароль")


@app.get("/api/users")
def get_users() -> Page[UserData]:
    all_users = [UserData.validate(user) for user in users.values()]
    return paginate(all_users)


@app.get("/api/users/{user_id}")
def get_user(user_id: int) -> UserData:
    if user_id in users:
        return users[user_id]
    else:
        raise HTTPException(status_code=404, detail=f"Пользователь с ид={user_id} не найден")


# @app.on_event("startup")

if __name__ == "__main__":
    import uvicorn

    add_pagination(app)
    users = load_json("test/users.json")
    dotenv.load_dotenv()
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))
