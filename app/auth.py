import time
from typing import Dict
from fastapi import HTTPException,Request,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from decouple import config
from sqlalchemy.orm import Session
from .models import *
from db_config import get_my_db

JWT_SECRET = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITM")





def sign_jwt(user_id: str) :
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print(token)

    return {
        "access_token":token
    }

def decode_jwt(token:str):
    try:
        payload = jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
    except:
        payload = None

    if payload:
        if payload["expires"] >= time.time():
            return payload
        raise HTTPException(status_code=403,detail="token expired")
    return{}




security = HTTPBearer()

def verify_jwt(token: str, db:Session):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        bkjwt = db.query(BlackList).filter(BlackList.jwt == token).first()
        if payload["expires"] < time.time():
            raise HTTPException(status_code=403, detail="Token expired")
        if bkjwt:
            raise HTTPException(status_code=403, detail="Please login")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


def jwt_required(credentials: HTTPAuthorizationCredentials = Depends(security), db:Session = Depends(get_my_db)):
    token = credentials.credentials
    return verify_jwt(token,db=db)