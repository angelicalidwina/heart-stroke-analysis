from fastapi import FastAPI
from database.data import engine
import uvicorn
from models import userModels, predictionModels
from routes.userRoutes import user_router
from routes.predictionRoutes import prediction_router

app = FastAPI()

userModels.Base.metadata.create_all(engine)
predictionModels.Base.metadata.create_all(engine)

app.include_router(user_router, prefix="/user")
app.include_router(prediction_router, prefix="/prediction")

@app.get('/')
def welcome() -> dict:
    return {"Message" : "Welcome to Heart Stroke Analysis"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)