from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseSettings

SQLALCHEMY_DATABASE_URL = 'sqlite:///./db.db'


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False}, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = "default"
    ALGORTIM: Optional[str] = "HS256"

    class Config:
        env_file = ".env"
