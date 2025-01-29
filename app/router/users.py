from http import HTTPStatus
from typing import Iterable

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page

from app.database.engine import engine
from app.database.users_db_service import UserDBService
from app.model.user import UserData, UserUpdate, UserCreate

router = APIRouter(prefix="/api/users")
service = UserDBService(engine)


@router.get("/all")
def get_users() -> Iterable[UserData]:
    """вернуть всех."""
    return service.get_users()


@router.get("/", )
def get_users_paginated() -> Page[UserData]:
    """постранично."""
    return service.get_users_paginated()


@router.get("/{user_id}")
def get_user(user_id: int) -> UserData:
    """вернуть одного по ид."""
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Недопустимый ид")
    user = service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Пользователь не найден")
    return user


@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate) -> UserData:
    # UserCreate.model_validate(user.model_dump())
    user_data = UserData(**user.model_dump())
    return service.create_user(user_data)


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: UserUpdate) -> UserData:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    # UserUpdate.model_validate(user.model_dump())
    return service.update_user(user_id, user)


@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    service.delete_user(user_id)
    return {"message": "User deleted"}
