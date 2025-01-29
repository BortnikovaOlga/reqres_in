from __future__ import annotations

from pydantic import EmailStr, BaseModel, HttpUrl
from sqlmodel import SQLModel, Field

from faker import Faker

fake = Faker()


class UserData(SQLModel, table=True, ):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl

    @staticmethod
    def random():
        return UserCreate(email=fake.email(),
                          first_name=fake.first_name(),
                          last_name=fake.last_name(),
                          avatar=fake.url())


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar: HttpUrl | None = None

    @staticmethod
    def random():
        return UserUpdate(email=fake.email(),
                          first_name=fake.first_name(),
                          last_name=fake.last_name(),
                          avatar=fake.url())
