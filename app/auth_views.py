from fastapi import APIRouter,Depends,HTTPException
from .schemas import *
from .auth import sign_jwt,decode_jwt
from sqlalchemy.orm import Session
from .models import UserModel
from db_config import get_my_db
from .helpers import hash_password,verify_password


auth = APIRouter()
users = []


def check_user(user_data):
    for user in users:
        if user['email'] == user_data.email and user['password'] == user_data.password:
            return True
    
    return False
    

@auth.post("/register")
async def register_views(user_data:UserSchema,db:Session = Depends(get_my_db)):
    oldemail = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if oldemail:
        raise HTTPException(status_code=400,detail="email alredy exist")
    pas_hash = hash_password(user_data.password)
    user = UserModel(username=user_data.username,email=user_data.email,password=pas_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"Message": "Registered User!"}


@auth.post("/login")
async def login_view(user_data: UserLoginSchema, db: Session = Depends(get_my_db)):
    user = db.query(UserModel).filter(UserModel.username == user_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = sign_jwt(user.email)
    return {"accsess_token":token}