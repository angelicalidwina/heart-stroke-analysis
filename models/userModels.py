from sqlalchemy import Column, String
from database.data import Base
from pydantic import BaseModel, EmailStr


class User(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key = True, index = True)
    username = Column(String)
    password = Column(String)

    class Config:
        schema_extra = {
            "example": {
                "username": "fastapi",
                "email": "fastapi@packt.com",
                "password": "strong!!!",
            }
        }


class SignUp(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "fastapi",
                "email": "fastapi@packt.com",
                "password": "strong!!!"
            }
        }

class Pengguna (BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "fastapi",
                "email": "fastapi@packt.com"
            }
        }

class TokenResponse(BaseModel):
    message: str
    access_token: str
    token_type: str

