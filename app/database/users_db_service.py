from __future__ import annotations

from typing import Iterable, List

from fastapi import HTTPException
from sqlmodel import Session, select
from app.model.user import UserData, UserUpdate
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate


class UserDBService:
    def __init__(self, engine):
        self.engine = engine

    def get_user(self, user_id: int) -> UserData | None:
        with Session(self.engine) as session:
            return session.get(UserData, user_id)

    def get_users(self) -> Iterable[UserData]:
        with Session(self.engine) as session:
            statement = select(UserData)
            return session.exec(statement).all()

    def get_users_paginated(self) -> Page[UserData]:
        with Session(self.engine) as session:
            statement = select(UserData)
            return paginate(session, statement)

    def get_user_by_email(self, email) -> UserData | None:
        with Session(self.engine) as session:
            statement = select(UserData).where(UserData.email == email)
            return session.exec(statement).first()

    def create_user(self, user: UserData) -> UserData:
        with Session(self.engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        return user

    def insert_users(self, users: List[UserData]):
        with Session(self.engine) as session:
            for user in users:
                session.add(user)
            session.commit()
            for user in users:
                session.refresh(user)
        return users

    def update_user(self, user_id: int, user: UserUpdate) -> UserData:
        with Session(self.engine) as session:
            db_user = session.get(UserData, user_id)
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            user_data = user.model_dump(exclude_unset=True)
            db_user.sqlmodel_update(user_data)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

    def delete_user(self, user_id: int):
        with Session(self.engine) as session:
            user = session.get(UserData, user_id)
            session.delete(user)
            session.commit()

    # todo
    # def delete_users(self, user_id: int):
    #     with Session(self.engine) as session:
    #         user = session.get(UserData, user_id)
    #         session.delete(user)
    #         session.commit()
