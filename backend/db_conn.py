import os

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

_engine = None
LocalSession = None
Base = declarative_base()


def _get_engine():
    """Create the app engine lazily so importing this module never requires DB_URL_AGENT."""
    global _engine, LocalSession
    if _engine is None:
        url = os.environ.get("DB_URL_AGENT")
        if not url:
            raise RuntimeError("DB_URL_AGENT is not set. Copy .env.example to .env and fill it in.")
        _engine = create_engine(url)
        LocalSession = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
    return _engine


def get_db():
    _get_engine()
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


def check_conn_db(db_password: str, db_name: str, db_user: str, db_host: str, db_port: str, driver_name: str):
    db_url = URL.create(
        drivername=driver_name,
        password=db_password,
        host=db_host or None,
        port=int(db_port) if db_port else None,
        username=db_user or None,
        database=db_name
    )
    try:
        connect_args = {} if driver_name.startswith("sqlite") else {"connect_timeout": 3}
        engine = create_engine(db_url, connect_args=connect_args)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
            return {"db_conn": True, "db_url": db_url}
    except SQLAlchemyError:
        return {"db_conn": False, "db_url": db_url}


def get_database(db_url: str):
    database = SQLDatabase.from_uri(db_url)
    return database
