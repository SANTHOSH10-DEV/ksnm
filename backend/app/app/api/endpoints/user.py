from fastapi import HTTPException,Depends, APIRouter,Body, Form
from sqlalchemy import or_
from typing import Annotated
from schemas import *
from models import * 
from database.session import SessionLocal
from datetime import datetime
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
from utils import user_name_verify,phone_number_validation, db_dependency,check
from core.security import get_password_hash

router=APIRouter()
def get_db(): 
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sign_up")
async def new_customer(db: Session = Depends(get_db),
                          first_name:str = Form(...),
                          last_name:str = Form(None),
                          full_name:str = Form(...),
                          phone_number:str = Form(...),
                          email_id:str = Form(...),
                          password: str = Form(...)):
    
    if user_name_verify(full_name, db):
        raise HTTPException(status_code=400, detail="User name already exists")

    if not phone_number_validation(phone_number):
        raise HTTPException(status_code=400, detail="Invalid phone number")
    
    already_exist_phone_number=db.query(Customer).filter(Customer.phone_number==phone_number).first()
    if already_exist_phone_number:
        return {"status" : 0 , "message" : "Phone number is aleady exist"}
    
    if not check(email_id):
        raise HTTPException(status_code=400, detail="Invalid email address")
    
    already_exist_email_id=db.query(Customer).filter(Customer.email_id==email_id).first()
    if already_exist_email_id:
        return {"status" :0, "message" : "email ID is already exist."}
    hashed_pass = get_password_hash(password)
    
    db_customer = Customer(
        first_name=first_name,
        last_name=last_name,
        full_name=full_name,
        phone_number=phone_number,
        email_id=email_id,
        password=hashed_pass,
        status=1,
        user_type= 4,
        created_at=datetime.now()
    )
    
    db.add(db_customer)
    
    db.commit()
    
    db.refresh(db_customer)
    
    return {
        "full_name": db_customer.full_name,
        "phone_number": db_customer.phone_number,
        "email_id": db_customer.email_id
    }

# Display All Customer
@router.get('/list_customer')
async def listCustomer(token : str,page_no:int,size:int,db:db_dependency):


    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()
    if not check_token:
        
        return {"message":"Token ID is not Activate"} 

      
    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session is expired'})


    user=db.query(Customer).filter(Customer.id==check_token.user_id,
                                   Customer.status==1,
                                   or_(Customer.user_type==1,Customer.user_type==2)).first()
    if not user:
        return {"status" : 0, "message": "Accessed only by 'SuperAdmin' or 'Admin'."}

    
    result=[]

    all_customer=db.query(Customer).all()

    if (len(all_customer)) % size == 0:
        total_page = int((len(all_customer))/size)
    else:
        total_page=((len(all_customer))//size+1)

    if total_page < page_no:
        return {"message" : f"Only {total_page} pages available" }

    line_no=(page_no-1)*size
    customers=db.query(Customer).offset(line_no).limit(size).all()
   
    # page_details=( "Page_no:", page_no, "Total_page:", 
    #               total_page,"Total_no_records:", len(all_customer))
    for user in customers:
        result.append(
            {
                "UserID" : user.id,
                "UserName" : user.full_name,
                "PhoneNumber" : user.phone_number,
                "UserEmailID" : user.email_id
            })

    return result

# # update Customer
@router.put('/update_customer')

async def update_customer(db: db_dependency, token:str = Form(...), 
                          first_name : str = Form(None),
                          last_name : str = Form(None),
                          full_name : str = Form(None),
                          phone_number : str = Form(None),
                          email_id : str = Form(None)):
    checkToken = db.query(ApiTokens).filter(ApiTokens.token == token).first()

    if checkToken.expires_at < datetime.now():
        checkToken.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session has expired. Please, Sign-in again Your ID'})


    if checkToken.status ==1:
        user=db.query(Customer).filter_by(id=checkToken.user_id).first()

        if first_name:
            user.first_name=first_name

        if last_name:
            user.last_name=last_name

        if full_name:
            if user_name_verify(full_name,db):
                raise HTTPException(status_code=400, detail="User name already exist")
            user.full_name=full_name

        if phone_number:
            if not phone_number_validation(phone_number):
                raise HTTPException(status_code=400, detail="Invalid Phone number")
            user.phone_number=phone_number

        if email_id:

            if not check(email_id):
                raise HTTPException(status_code=400, detail="Invalid email address")
            user.email_id=email_id
        
        db.commit()
        db.refresh(user)
        # return user
        return ({
            "UserID" : user.id,
            "FirstName" : user.first_name,
            "LastName" : user.last_name,
            "FullName" : user.full_name,
            "PhoneNumber" : user.phone_number,
            "email_id" : user.email_id
        })
    
@router.delete("delete_customer_ID")
async def deleteUser(token:str,full_name:str, db:db_dependency):
    
    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()

    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session has expired. Please, Sign-in again Your ID'})


    if not check_token:
        
        return {"message":"Token ID is not Activate"} 
    
    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session is expired'})

    if check_token.status ==1:
        user=db.query(Customer).filter(Customer.id==check_token.user_id,
                                       Customer.full_name==full_name).first()
        user.status = 0
        
        db.commit()

        return {"message" : "UserID successfully deactivated."}

