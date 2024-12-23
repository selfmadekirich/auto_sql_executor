from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: str | None = None


class User(BaseModel):
    username: str
    scopes: str | None = None


class UserSingUp(BaseModel):
    username: str
    password: str
    scopes: str | None = None


class UserInDB(User):
    username: str
    hashed_password: str
    scopes: str | None = None
