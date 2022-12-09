from database.data import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status
from models.predictionModels import Prediction, InputData
from sqlalchemy.orm import Session
from auth.authenticate import authenticate
import sys

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

prediction_router = APIRouter(
    tags=['Prediction'],
)

@prediction_router.post("/input")
def input_data(request:InputData, db: Session = Depends(get_db), user: str = Depends(authenticate) ) -> dict:
    prediksi = db.query(Prediction.email).filter(Prediction.email == user).scalar()

    if prediksi:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Data sudah ada. Silahkan lakukan update")

    user_age = request.age
    user_height = request.height
    user_weight = request.weight
    user_bmi = round(user_weight/(user_height * user_height), 2)
    if user_bmi < 18.5:
        user_kategori_bmi = "Underweight"
    elif user_bmi >= 18.5 and user_bmi < 24.9:
        user_kategori_bmi = "Normal weight"
    elif user_bmi >= 25.0 and user_bmi < 29.9:
        user_kategori_bmi = "Overweight"
    elif user_bmi >= 30.0 and user_bmi < 39.9:
        user_kategori_bmi = "Obese"
    elif user_bmi >= 40.0:
        user_kategori_bmi = "Morbidly Obese"
    user_glucose = request.glucose
    user_cholesterol = request.cholesterol
    if user_age >= 35 :
        if user_bmi == 'Overweight' or user_bmi == 'Obese' or user_bmi == 'Morbidly Obese':
            if user_glucose >= 150 and user_cholesterol >= 200:
                user_chance = 'High'
            elif user_glucose >= 150 and user_cholesterol < 200:
                user_chance = 'High'
            elif user_glucose < 150 and user_cholesterol >=200:
                user_chance = 'High'
            elif user_glucose < 150 and user_cholesterol < 200:
                user_chance = 'Possible'
        else:
            if user_glucose >= 150 and user_cholesterol >= 200:
                user_chance = 'High'
            elif user_glucose >= 150 and user_cholesterol < 200:
                user_chance = 'Possible'
            elif user_glucose < 150 and user_cholesterol >= 200:
                user_chance = 'Possible'
            elif user_glucose < 150 and user_cholesterol < 200:
                user_chance = 'Low'
    else:
        if user_bmi == 'Overweight' or user_bmi == 'Obese' or user_bmi == 'Morbidly Obese':
            if user_glucose >= 150 and user_cholesterol >= 200:
                user_chance = 'High'
            elif user_glucose >= 150 and user_cholesterol < 200:
                user_chance = 'Possible'
            elif user_glucose < 150 and user_cholesterol >=200:
                user_chance = 'Possible'
            elif user_glucose < 150 and user_cholesterol < 200:
                user_chance = 'Low'
        else:
            if user_glucose >= 150 and user_cholesterol >= 200:
                user_chance = 'Possible'
            elif user_glucose >= 150 and user_cholesterol < 200:
                user_chance = 'Low'
            elif user_glucose < 150 and user_cholesterol >= 200:
                user_chance = 'Low'
            elif user_glucose < 150 and user_cholesterol < 200:
                user_chance = 'Low'

    new_prediction = Prediction(email = user, age = user_age, height=user_height, 
                                        weight=user_weight, bmi=user_bmi, kategori_bmi = user_kategori_bmi,
                                        glucose = user_glucose, cholesterol=user_cholesterol, chance=user_chance)
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    return {"bmi": user_bmi, "kategori_bmi": user_kategori_bmi, "chance": user_chance}


@prediction_router.get("/result")
def get_prediction(db: Session = Depends(get_db), user: str = Depends(authenticate))-> dict:
    prediksi = db.query(Prediction.email).filter(Prediction.email == user).scalar()
    
    if not prediksi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

    user_bmi = db.query(Prediction.bmi).filter(Prediction.email ==  user).scalar()
    user_kategori = db.query(Prediction.kategori_bmi).filter(Prediction.email == user).scalar()
    user_chance = db.query(Prediction.chance).filter(Prediction.email == user).scalar()
    sys.setrecursionlimit(10000)
    return {"email": prediksi, "bmi": user_bmi, "kategori_bmi": user_kategori, "chance": user_chance}

@prediction_router.get('/recommendation')
def get_recommendation(db: Session = Depends(get_db), user : str = Depends(authenticate)) -> dict:
    prediksi = db.query(Prediction.chance).filter(Prediction.email == user).scalar()
    glucose = db.query(Prediction.glucose).filter(Prediction.email == user).scalar()
    cholesterol = db.query(Prediction.cholesterol).filter(Prediction.email == user).scalar()
    
    if not prediksi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    if prediksi == 'Low':
        if glucose < 150 and cholesterol <200:
            return{"Message" : "Overall, your health is good, but don't forget to exercise!!"}
        if glucose >= 150 and cholesterol <200:
            return{'Message': 'Overall, your health is good but your glucose level is high. Therefore you have to pay attention to carbohydrate intake, consume foods high in fiber, exercise regularly, and reduce sweet foods'}
        if glucose <150 and cholesterol >=200:
            return{'Message': 'Overall, your health is good but your cholesterol level is high. Therefore, exercise regularly, avoid foods that trigger hypertension and cholesterol and reduce your intake of salt, saturated fat and trans fat.'}
    if prediksi == 'Possible':
        if glucose >= 150 and cholesterol >=200:
            return{"Message" : "You have a chance of having a heart attack. Your glucose and cholesterol levels are high. You have to pay attention to your food intake and get lots of exercise"}
        if glucose >= 150 and cholesterol <200:
            return{'Message': 'You have a chance of having a heart attack and your glucose levels are high. Therefore you have to pay attention to carbohydrate intake, consume foods high in fiber, exercise regularly, and reduce sweet foods'}
        if glucose <150 and cholesterol >=200:
            return {'Message' : 'You have a chance of having a heart attack and your cholesterol level is high. Therefore, exercise regularly, avoid foods that trigger hypertension and cholesterol and reduce your intake of salt, saturated fat and trans fat.'}
    if prediksi == 'High':
        if glucose >= 150 and cholesterol >=200:
            return{"Message" : "You have a high chance of having a heart attack. Your glucose and cholesterol levels are high. You have to pay attention to your food intake and get lots of exercise"}
        if glucose >= 150 and cholesterol <200:
            return{'Message': 'You have a high chance of having a heart attack and your glucose levels are high. Therefore you have to pay attention to carbohydrate intake, consume foods high in fiber, exercise regularly, and reduce sweet foods'}
        if glucose <150 and cholesterol >=200:
            return {'Message' : 'You have a high chance of having a heart attack and your cholesterol level is high. Therefore, exercise regularly, avoid foods that trigger hypertension and cholesterol and reduce your intake of salt, saturated fat and trans fat.'}

@prediction_router.delete('/delete')
def delete_data(db: Session = Depends(get_db), user : str = Depends(authenticate)) -> dict:
    prediksi = db.query(Prediction).filter(Prediction.email == user)
    
    if not prediksi.scalar():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    prediksi.delete()
    db.commit()
    return {"Message" : "Data deleted successfully"}
    

@prediction_router.put("/update")
def update_data(request:InputData, db: Session = Depends(get_db), user: str = Depends(authenticate)) -> dict:
    update_prediksi = db.query(Prediction).filter(Prediction.email == user)

    if not update_prediksi.scalar():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    user_age = request.age
    user_height = request.height
    user_weight = request.weight
    user_bmi = round(user_weight/(user_height * user_height), 2)
    if user_bmi < 18.5:
        user_kategori_bmi = "Underweight"
    elif user_bmi >= 18.5 and user_bmi < 24.9:
        user_kategori_bmi = "Normal weight"
    elif user_bmi >= 25.0 and user_bmi < 29.9:
        user_kategori_bmi = "Overweight"
    elif user_bmi >= 30.0 and user_bmi < 39.9:
        user_kategori_bmi = "Obese"
    elif user_bmi >= 40.0:
        user_kategori_bmi = "Morbidly Obese"
    user_glucose = request.glucose
    user_cholesterol = request.cholesterol
    if user_age >= 35 :
        if user_bmi == 'Overweight' or user_bmi == 'Obese' or user_bmi == 'Morbidly Obese':
            if user_glucose >= 150 and user_cholesterol >= 200:
                user_chance = 'High'
            elif user_glucose >= 150 and user_cholesterol < 200:
                user_chance = 'High'
            elif user_glucose < 150 and user_cholesterol >=200:
                user_chance = 'High'
            elif user_glucose < 150 and user_cholesterol < 200:
                user_chance = 'Possible'
        else:
            if user_glucose >= 150 and user_cholesterol >= 200:
                user_chance = 'High'
            elif user_glucose >= 150 and user_cholesterol < 200:
                user_chance = 'Possible'
            elif user_glucose < 150 and user_cholesterol >= 200:
                user_chance = 'Possible'
            elif user_glucose < 150 and user_cholesterol < 200:
                user_chance = 'Low'
    else:
        if user_bmi == 'Overweight' or user_bmi == 'Obese' or user_bmi == 'Morbidly Obese':
            if user_glucose >= 150 and user_cholesterol >= 200:
                user_chance = 'High'
            elif user_glucose >= 150 and user_cholesterol < 200:
                user_chance = 'Possible'
            elif user_glucose < 150 and user_cholesterol >=200:
                user_chance = 'Possible'
            elif user_glucose < 150 and user_cholesterol < 200:
                user_chance = 'Low'
        else:
            if user_glucose >= 150 and user_cholesterol >= 200:
                user_chance = 'Possible'
            elif user_glucose >= 150 and user_cholesterol < 200:
                user_chance = 'Low'
            elif user_glucose < 150 and user_cholesterol >= 200:
                user_chance = 'Low'
            elif user_glucose < 150 and user_cholesterol < 200:
                user_chance = 'Low'

    update_prediksi.update({'age':user_age, 'height':user_height, 'weight': user_weight,
                            'bmi':user_bmi, 'kategori_bmi':user_kategori_bmi, 
                            'glucose': user_glucose, 'cholesterol':user_cholesterol, 'chance':user_chance})
    db.commit()
    return {"Message": "Data successfully updated", "bmi": user_bmi, "kategori_bmi": user_kategori_bmi, "chance": user_chance}

@prediction_router.get('/analysis')
def count_chance(db: Session =  Depends(get_db)):
    count_chance_low = db.query(Prediction).filter_by(chance = 'Low')
    count_low = count_chance_low.count()
    count_chance_high = db.query(Prediction).filter_by(chance = 'High')
    count_high = count_chance_high.count()
    count_chance_possible = db.query(Prediction).filter_by(chance = 'Possible')
    count_possible = count_chance_possible.count()

    return {
        'Number of people with low heart attack rates' : count_low,
        'Number of people with possible heart attack rates':count_possible,
        'Number of people with high heart attack rates' : count_high
    }

