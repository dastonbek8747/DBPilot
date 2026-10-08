import os
import uvicorn
from dark_swag import FastAPI as DarkFastAPI
from fastapi import Depends, Response
from db_conn import get_db, Base, enginge, check_conn_db
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from hashing_password import generate_session_id, verify_password, hashing_password
from ai_models import chat_agent, get_chat_history
import jwt

app = DarkFastAPI()
app.mount(
    "/creating_files",
    StaticFiles(directory="creating_files")
)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

Base.metadata.create_all(enginge)


@app.post("/test")
async def root():
    return {"message": "Hello World"}


@app.get("/get_chat_history")
async def get_history(session_id: str):
    return get_chat_history(session_id=session_id)


@app.post("/chat_agent")
async def get_chat_agent(request: schemas.ChatAgent):
    response = chat_agent(session_id=request.session_id, request=request.request, database_url=request.database_url)
    return response


@app.post("/check_db")
async def check_db(db: schemas.DatabaseConnection):
    response = check_conn_db(db_name=db.db_name, db_user=db.db_user, db_host=db.db_host,
                             db_port=db.db_port, db_password=db.db_password, driver_name=db.driver_name)
    return {"messages": response}


@app.post("/signin")
async def signin(request: schemas.RegisterUser, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.email == request.email).first()
    if db_user:
        return {"message": "Email already registered"}
    else:
        new_user = models.Users(
            email=request.email,
            username=request.username,
            session_id=generate_session_id(),
            password=hashing_password(request.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "message": "User created successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "session_id": new_user.session_id
            }
        }


@app.post("/login")
async def login(request: schemas.LoginUser, response: Response, db: Session = Depends(get_db)):
    db_uer = db.query(models.Users).filter(models.Users.email == request.email).first()
    if db_uer:
        if verify_password(request.password, db_uer.password):
            encoded_jwt = jwt.encode(key=os.environ.get("SECRET_KEY"), payload={"user_id": db_uer.id},
                                     algorithm='HS256')
            response.set_cookie(key="access_token", value=encoded_jwt, httponly=False, secure=False, samesite="strict")
            return {"message": "Login successful", "user": db_uer}
        else:
            return {"message": "Invalid credentials"}
    else:
        return {"message": "User not found"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
