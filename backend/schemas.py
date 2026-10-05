from pydantic import BaseModel, Field, EmailStr


class RegisterUser(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=30)
class ChatAgent(BaseModel):
    session_id: str
    database_url:str
    request:str

class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=30)


class UserConnectionDatabases(BaseModel):
    db_name: str
    db_url: str
class DatabaseConnection(BaseModel):
    driver_name: str
    db_name: str
    db_user: str
    db_host: str
    db_port: str
    db_password: str