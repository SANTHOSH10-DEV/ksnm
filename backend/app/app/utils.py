from database.session import SessionLocal
from fastapi import Depends, HTTPException #,FastAPI, status,APIRouter,Query
from models import * 
from email_validator import validate_email, EmailNotValidError

from typing import Annotated
from sqlalchemy.orm import Session




def get_db(): 
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency= Annotated[Session, Depends(get_db)]


def check(email):
    try:
        v = validate_email(email)
        email = v["email"]
        return True
    except EmailNotValidError:
        return False


def user_name_verify(name:str,db:db_dependency) -> bool:
    db_users=db.query(Customer).filter(Customer.full_name==name).first()
    if db_users:
        return True
    else:
        return False 

def phone_number_validation(number:str):
   
    num=number.replace(" ","")
    if num[0] in ['6','7','8','9'] and len(num)==10 and int(num)*0.5==int(num)/2:
        return True
    else:
        return False
   
    

