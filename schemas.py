from pydantic import BaseModel, Field, EmailStr


class RegisterUser(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=30)


class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=30)


class UserConnectionDatabases(BaseModel):
    db_name: str
    db_url: str
