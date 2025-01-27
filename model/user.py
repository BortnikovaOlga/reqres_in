from pydantic import BaseModel, Field


class UserData(BaseModel):
    id: int = Field(...,)
    email: str = Field(...,)
    first_name: str = Field(...,)
    last_name: str = Field(...,)
    avatar: str = Field(...,)

