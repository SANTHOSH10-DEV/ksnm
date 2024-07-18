from fastapi import HTTPException, APIRouter, Form, Query, Body, Depends
from sqlalchemy import or_
from typing import Annotated
from schemas import *
from models import * 
from datetime import datetime


from utils import db_dependency

router=APIRouter()


# Add New Product_type
@router.post("/create_producttype")
async def create_product_type(token : str, producttype_name:str, db:db_dependency):

    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()
    if not check_token:
        
        return {"message":"Token ID is not Activate"} 
    
    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session is expired. Please, Sign-in Your ID'})

    user=db.query(Customer).filter(Customer.id==check_token.user_id,
                                   Customer.status==1,
                                   or_(Customer.user_type==1,Customer.user_type==2)).first()
    if not user:
        return {"status" : 0, "message": "Accessed only by 'SuperAdmin' or 'Admin' "}
    

    already_exist=db.query(Producttype).filter_by(name=producttype_name,
                                                  status=1).first()
    if already_exist:
        return {"message":"This Product type name is already exist"}
    db_producttype=Producttype(name=producttype_name,date=datetime.now(),status=1)
    db.add(db_producttype)
    db.commit()
    return db_producttype

#Display Product type
@router.get('/list_producttype')
async def listProductTypes(token:str,db:db_dependency):

    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()
    if not check_token:
        
        return {"message":"Token ID is not Activate"} 

    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session is expired. Please, Sign-in Your ID'})


    user=db.query(Customer).filter(Customer.id==check_token.user_id,
                                   Customer.status==1,
                                   or_(Customer.user_type==1,Customer.user_type==2)).first()
    if not user:
        return {"status" : 0, "message": "Accessed only by 'SuperAdmin' or 'Admin' "}
    
    
    if check_token.status ==1:
        all_producttype=db.query(Producttype).all()
        return all_producttype
    else:
        return {"message":"Token ID is not Activate"} 
    

# Update product_types
@router.put("/product_details_update")
async def update_produtType_details(token : str,
                                    product_type_it:int = Form(...,),
                                    name : str = Form(...,),
                                    db : db_dependency = None):
    
    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()
    if not check_token:
        
        return {"message":"Token ID is not Activate"} 

    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session is expired. Please, Sign-in Your ID'})

    
    user=db.query(Customer).filter(Customer.id==check_token.user_id,
                                   Customer.status==1,
                                   or_(Customer.user_type==1,Customer.user_type==2)).first()
    if not user:
        return {"status" : 0, "message": "Accessed only by 'SuperAdmin' or 'Admin' "}
    

    getProducttypeDetail=db.query(Producttype).filter(Producttype.id==product_type_it).one()
    if not getProducttypeDetail:
        return {"message":"Product_ID is not found"}
    else:
        if name:
            getProducttypeDetail.name=name
        
        db.commit()
    
        return ({"Product_ID": product_type_it,"status": 1, "msg":"Successfully Updated"})
