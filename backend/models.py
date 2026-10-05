from sqlalchemy import Column, Integer, String, ForeignKey
from db_conn import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    session_id = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, index=True, nullable=False)


class DatabaseUsers(Base):
    __tablename__ = 'database_users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    db_name = Column(String, index=True)
    db_url = Column(String, index=True)
