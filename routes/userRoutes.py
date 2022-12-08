from database.data import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, status
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from auth.authenticate import authenticate
from fastapi.security import OAuth2PasswordRequestForm
from models.userModels import TokenResponse, User, SignUp, Pengguna
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_router = APIRouter(
    tags=["User"],
)


@user_router.post("/signup")
def sign_user_up(request: SignUp, db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.email == request.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists"
        )

    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must have at least 8 character"
        )

    hashed_password = HashPassword().create_hash(request.password)
    new_user = User(email=request.email, username=request.username,
                    password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User successfully registered!"
    }

@user_router.post("/signin", response_model=TokenResponse)
def sign_user_in(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    if not HashPassword().verify_hash(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Wrong credential passed")

    access_token = create_access_token(user.email)

    return {"message" : "User successfully signin", "access_token": access_token, "token_type": "bearer"}

@user_router.get('/users', response_model=list[Pengguna])
def get_all_user(db :  Session = Depends(get_db), user: str = Depends(authenticate)):
    admin = db.query(User.email).filter_by(email = 'admin@gmail.com')
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    
    return db.query(User).all()