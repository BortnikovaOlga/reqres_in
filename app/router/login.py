from fastapi import APIRouter, HTTPException

from app.database.engine import engine
from app.database.users_db_service import UserDBService
from app.model.auth import AuthData, LoginResponse
from auth_db import auth_db

router = APIRouter()
service = UserDBService(engine)


@router.post("/api/login")
def login(auth: AuthData) -> LoginResponse:
    """пока нет auth таблицы, пароль из словаря."""
    # todo auth-таблица
    if service.get_user_by_email(auth.email) and auth.password == auth_db[auth.email]:
        return LoginResponse(token="QpwL5tke4Pnpja7X4")
    else:
        raise HTTPException(status_code=400, detail="неверный логин или пароль")
