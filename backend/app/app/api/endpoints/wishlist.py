from fastapi import HTTPException, APIRouter,Body, Depends
from schemas import *
from models import * 
from datetime import datetime

from utils import db_dependency

router=APIRouter()

#customer add products in wishlist
@router.post('/wishlist')
async def add_wihslish(token:str,product_id:int,db:db_dependency):
    
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

    already_exist=db.query(Wishlist).filter(Wishlist.customer_id==check_token.user_id,
                                            Wishlist.product_id==product_id,
                                            Wishlist.status==1).first()
    if already_exist:
        return {"message":"This Product is already added to wishlist"}
    proId_in_pro_table=db.query(Product).filter(Product.id==product_id,Product.status==1).first()
    if not proId_in_pro_table:
        return {"message" : "This Product doesn't exist in Product Table"}
    db_list=Wishlist(customer_id=check_token.user_id,product_id=product_id,
                     date=datetime.now(),status=1)
    
    db.add(db_list)
    db.commit()
    db.refresh(db_list)

    result=[{
        "WishlistID" : db_list.id,
        "CustomerID" : db_list.customer_id,
        "ProductID" : db_list.product_id
            }]
    
    return result

#Display in wishlist
@router.post('/ListWishlist')
async def list_wihslish(token:str,db:db_dependency):
    
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

    result=[]

    filter_data=db.query(Wishlist).filter(Wishlist.customer_id==check_token.user_id,
                                            Wishlist.status==1).all()
    if filter_data:
        for db_list in filter_data:
            result.append({
                "wishlist_id" : db_list.id,
                "Customer_id": db_list.customer_id,
                "Product_id" : db_list.product_id,
            }) 
        return result
    else:
        return {"message" : "Null"}


#customer remove products in wishlist
@router.post('/delete_wishlist')
async def delete_wihslish(token:str,product_id:int,db:db_dependency):
    
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

    removeId=db.query(Wishlist).filter(Wishlist.customer_id==check_token.user_id,
                                           Wishlist.product_id==product_id).first()
    if removeId:
        removeId.status= 0
        db.commit()
        return {"message": "successfully deleted"}
    else:
        return {"message" : "Product ID not exist"}
