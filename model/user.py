from pydantic import BaseModel, Field


class UserData(BaseModel):
    id: int = Field(..., )
    email: str = Field(..., )
    first_name: str = Field(..., )
    last_name: str = Field(..., )
    avatar: str = Field(..., )


class UsersDataPage(BaseModel):
    items: list[UserData]
    size: int
    page: int
    total: int
    pages: int | None = Field(default=None)
