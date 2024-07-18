from fastapi import HTTPException, APIRouter, Form, Query, Body, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Annotated
from schemas import *
from models import * 
from datetime import datetime


from utils import db_dependency

router=APIRouter()


# Add new Product
@router.post("/NewProduct")
async def new_product(token:str, product_name : str, product_type: int,
                      rate : float, db:db_dependency):

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
    

    already_exist=db.query(Product).filter(Product.name==product_name,
                                           Product.pro_type==product_type,
                                           Product.rate==rate).first()
    if already_exist:
        return {"message":"This Product name is already exist"}
    db_product=Product(name=product_name,pro_type=product_type,rate=rate,
                       date=datetime.now(),status=1)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


#update product_details
@router.put("/product_details_update")
async def update_product_details(token : str, product_it:int,
                              name : str = Form(None),
                              product_type : int = Form(None),
                              rate : float = Form(None),
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
    

    getProductDetail=db.query(Product).filter(Product.id==product_it).one()
    if not getProductDetail:
        return {"message":"Product_ID is not found"}
    else:
        if name:
            getProductDetail.name=name
        if product_type:
            getProductDetail.pro_type=product_type
        if rate:
            getProductDetail.rate=rate
        db.commit()
    
        return ({"Product_ID": product_it, "msg":"Successfully Updated"})



# #Display all product
# @router.post('/product')
# async def list_products(db:db_dependency,token:str = Form(...),ProductType :str = Form(None), Search : str = Form(None)):
#     checkToken = db.query(ApiTokens).filter(ApiTokens.token == token).first()
#     if checkToken.status ==1:
#         if ProductType and Search:
#             TypeName=db.query(Producttype).filter(Producttype.name==ProductType).first()
#             if TypeName:
#                 pro_find=db.query(Product).filter(Product.pro_type==TypeName.id,Product.name==Search).first()
#                 if pro_find:
#                     return pro_find
#                 return {"msg" : "Product name is not exist"}
#             return {"msg" : "Product Type name is not exist"}
        
#         elif ProductType:
#             TypeName=db.query(Producttype).filter(Producttype.name==ProductType).first()
#             if TypeName:
#                 pro_find=db.query(Product).filter(Product.pro_type==TypeName.id).first()
#                 if pro_find is None:
#                     return {"message":"Product not found"}
#                 return pro_find
#             return {"message" : "Product Type name is not found"}
#         elif Search:
#             pro_find=db.query(Product).filter(Product.name==Search).first()
#             if pro_find is None:
#                 return {"message":"Product not found"}
#             return pro_find
#         else:
#             all_product=db.query(Product).all()
#             return all_product
#     else:
#         return {"message":"Token ID is not Activate"} 


#Display all product
@router.post('/listProduct')
async def list_products(token:str,db:db_dependency,
                        ProductType :str = Form(None) ,
                          Search : str = Form(None) ):
  
    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()
    if not check_token:
        
        return {"message":"Token ID is not Activate"} 
    
    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session is expired. Please, Sign-in Your ID'})
   

    if ProductType and Search:
        TypeName=db.query(Producttype).filter(Producttype.name==ProductType).first()
        if TypeName:
            pro_find=db.query(Product).filter(Product.pro_type==TypeName.id,Product.name==Search).first()
            if pro_find:
                return pro_find
            return {"msg" : "Product name doesn't exist"}
        return {"msg" : "Product Type name doesn't exist"}
    
    elif ProductType:
        TypeName=db.query(Producttype).filter(Producttype.name==ProductType).first()
        if TypeName:
            pro_find=db.query(Product).filter(Product.pro_type==TypeName.id).all()
            if pro_find is None:
                return {"message":"Product not found"}
            return pro_find
        return {"message" : "Product Type name doesn't found"}
    elif Search:
        pro_find=db.query(Product).filter(Product.name==Search).first()
        if pro_find is None:
            return {"message":"Product not found"}
        return pro_find
    else:
        all_product=db.query(Product).all()
        return all_product

