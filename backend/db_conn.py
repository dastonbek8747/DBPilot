from sqlalchemy import create_engine, text, URL
from sqlalchemy.exc import SQLAlchemyError
from langchain_community.utilities import SQLDatabase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()
enginge = create_engine(os.environ.get("DB_URL_AGENT"))
LocalSession = sessionmaker(bind=enginge, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


def check_conn_db(db_password: str, db_name: str, db_user: str, db_host: str, db_port: str, driver_name: str):
    db_url = URL.create(
        drivername=driver_name,
        password=db_password,
        host=db_host,
        port=int(db_port),
        username=db_user,
        database=db_name
    )
    try:
        engine = create_engine(db_url, connect_args={"connect_timeout": 3})
        with engine.connect() as conn:
            conn.execute(text("SELECT version();"))
            return {"db_conn": True, "db_url": db_url}
    except SQLAlchemyError as e:
        return {"db_conn": False, "db_url": db_url}


def get_database(db_url: str):
    database = SQLDatabase.from_uri(db_url)
    return database
