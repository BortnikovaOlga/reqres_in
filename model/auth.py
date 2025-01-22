from pydantic import BaseModel


class AuthData(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str = "QpwL5tke4Pnpja7X4"


class LoginError(BaseModel):
    error: str
