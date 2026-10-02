import uvicorn
from dark_swag import FastAPI as DarkFastAPI
from fastapi import Depends
from db_conn import get_db, Base, enginge
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models
import schemas
from hashing_password import generate_session_id, verify_password, hashing_password
from ai_models import chat_agent, get_chat_history

app = DarkFastAPI()
app.mount(
    "/creating_files",
    StaticFiles(directory="creating_files", html=True)
)

Base.metadata.create_all(enginge)


@app.post("/test")
async def root():
    return {"message": "Hello World"}


@app.get("/get_chat_history")
async def get_history(session_id: str):
    return get_chat_history(session_id=session_id)


@app.post("/chat_agent")
async def get_chat_agent(session_id: str, db_url: str, request: str):
    response = chat_agent(session_id=session_id, request=request, database_url=db_url)
    return response


@app.post("/signin")
async def signin(request: schemas.RegisterUser, db: Session = Depends(get_db)):
    new_email = request.email
    check_email = db.query(models.Users).filter(models.Users.email == new_email).first()
    if check_email:
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
        db.close()
        return {"message": "User created successfully"}


@app.post("/login")
async def login(request: schemas.LoginUser, db: Session = Depends(get_db)):
    db_uer = db.query(models.Users).filter(models.Users.email == request.email).first()
    if db_uer:
        if verify_password(request.password, db_uer.password):
            return {"message": "Login successful", "user": db_uer}
        else:
            return {"message": "Invalid credentials"}
    else:
        return {"message": "User not found"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
