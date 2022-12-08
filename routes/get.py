@prediction_router.put("/updatedata", response_model=ShowPrediction)
def update_data(request:InputData, db: Session = Depends(get_db), user: str = Depends(authenticate) ) -> dict:
    user = db.query(User.email)
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
    if user_glucose >= 150 and user_cholesterol >= 200:
        user_chance = "High"
    elif user_glucose < 150 and user_cholesterol >= 200:
        user_chance = "High"
    elif user_glucose >= 150 and user_cholesterol < 200:
        user_chance = "High"
    elif user_glucose < 150 and user_cholesterol < 200:
        user_chance = "Low"
    
    updatedata = db.query(Prediction).filter(Prediction.email == user)
    updatedata.update({'age': user_age})
    updatedata.update({'height': user_height})
    updatedata.update({'weight':user_weight})
    updatedata.update({'bmi': user_bmi})
    updatedata.update({'kategori_bmi':user_kategori_bmi})
    updatedata.update({'glucose':user_glucose})
    updatedata.update({'cholesterol':user_cholesterol})
    updatedata.update({'chance':user_chance})

    db.commit()
    return {"bmi": user_bmi, "kategori_bmi": user_kategori_bmi, "chance": user_chance}

@prediction_router.post("/inputdata", response_model=ShowPrediction)
def input_data(request:InputData, db: Session = Depends(get_db), user: str = Depends(authenticate) ) -> dict:
    user = db.query(User.email)
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
    if user_glucose >= 150 and user_cholesterol >= 200:
        user_chance = "High"
    elif user_glucose < 150 and user_cholesterol >= 200:
        user_chance = "High"
    elif user_glucose >= 150 and user_cholesterol < 200:
        user_chance = "High"
    elif user_glucose < 150 and user_cholesterol < 200:
        user_chance = "Low"
    
    new_prediction = Prediction(email = user, age = user_age, height=user_height, 
                                weight=user_weight, bmi=user_bmi, kategori_bmi = user_kategori_bmi,
                                glucose = user_glucose, cholesterol=user_cholesterol, chance=user_chance)
    db.add(new_prediction)
    db.commit()
    return {"bmi": user_bmi, "kategori_bmi": user_kategori_bmi, "chance": user_chance}
