from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database.data import Base
from pydantic import BaseModel

class Prediction(Base):
    __tablename__ = "prediction"

    id = Column(Integer, primary_key=True)
    email = Column(String, ForeignKey("users.email"), unique=True, index=True)
    age = Column(Integer)
    height_meter = Column(Float)
    weight = Column(Integer)
    bmi = Column(Float, default="")
    kategori_bmi = Column(String, default="")
    glucose = Column(Integer)
    cholesterol = Column(Integer)
    chance = Column(String, default="")

    class Config:
        schema_extra = {
            "example": {
                "age": 20,
                "height": 1.5,
                "weight": 45.0,
                "glucose": 120,
                "cholesterol": 100
            }
        }

class InputData(BaseModel):
    age : int
    height_meter: float
    weight : float
    glucose: int
    cholesterol: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "age" : 20,
                "height_meter": 1.5,
                "weight": 45.0,
                "glucose": 120,
                "cholesterol": 100
            }
        }

