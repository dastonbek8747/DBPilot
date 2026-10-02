import uvicorn
from dark_swag import FastAPI as DarkFastAPI
from fastapi import Depends
from db_conn import get_db, Base
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


@app.post("/test")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
