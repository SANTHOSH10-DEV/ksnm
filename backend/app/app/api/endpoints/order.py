from sqlalchemy import or_
from fastapi import HTTPException,Depends, APIRouter,Body,Form,Query
from typing import Annotated
from schemas import *
from models import * 
from database.session import SessionLocal
from datetime import datetime,date
from sqlalchemy.orm import Session


from utils import db_dependency


router=APIRouter()


@router.post('/OderList')
async def order_history(token:str,db:db_dependency):

    check_token=db.query(ApiTokens).filter(ApiTokens.token==token).first()
       
    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session has expired. Please, Sign-in again Your ID'})


    if not check_token:
        
        return {"message":"Token ID is not Activate"} 
 
    
    if check_token.status ==1:
        db_list=db.query(Cart).filter(Cart.customer_id==check_token.user_id,
                                                Cart.status==-1).all()
        
        # if db_list is None:
        #     return {"message" : "Your Order History is Empty"}
        result=[]
        for data in db_list:
            date=data.date
            result.append({                
                "ProductID" : data.product_id,
                "Quantity" : data.quantity,
                "Total" : data.total,
                "Date" : date.date()
            })
        if not result:
            return {"Status" : 0, "message" : "Order List is Empty"}

        return result 
    else:
        return {"message" : "Token ID is not Activate"} 
    



@router.post('/OrderList')
async def order_list(token:str,db:db_dependency):
    
    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()
       
    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session is expired'})


    if not check_token:
        
        return {"message":"Token ID is not Activate"} 
 
    if check_token.status ==1:
        result=[]
        db_list=db.query(Sales).filter(Sales.customer_id==check_token.user_id,
                                                Sales.status==1).all()
        
        if db_list:
            for data in db_list:
                result.append(
                    {
                        "OrderID" : data.id,
                        "Address" : data.address,
                        "Payment Type" : data.payment_type,
                        "Total Amount" : data.total_amount,
                        "Date" : data.date.date()

                    }
                )
            return {
                "Customer Id" : check_token.user_id,
                "Customer Name" : check_token.customer.full_name,
                "Order List" : result

                }
        else:
            return {"message" : "Your Order List is Empty"}
    else:
        return {"message":"Token ID is not Activate"} 
    



@router.post('/OrderDetails')
async def order_details(token:str, sales_id: int,db:db_dependency):
    
    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()

    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session has expired. Please, login again to continue.'})
    
    if not check_token:
        
        return {"message":"Token ID is not Activate"} 
    
    result=[]
    filtersalesID=db.query(Salesdetails
                            ).filter_by(sales_id=sales_id,
                                        status=1).all()
    if filtersalesID:
        for eachdetails in filtersalesID:
            result.append({
                "SalesID" : eachdetails.id,
                "ProductID" : eachdetails.product_id,
                "Quantity" : eachdetails.quantity,
                "Rate" : eachdetails.rate,
                "Total" : eachdetails.total,
                "DateTime" : eachdetails.date })

        return result
    else:
        return {"Staus": 0, "message" : "Invalied Sales_id"}


# orderstatus update
@router.post('/OrderStatusUpdate')
async def order_status_update(token:str, sales_id: int,update_status: Annotated[int, Query(le=3)],db:db_dependency):

    check_token = db.query(ApiTokens).filter(ApiTokens.token == token).first()
 
    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session is expired'})

    if not check_token:
        
        return {"message":"Token ID is not Activate"} 
     
      
    user=db.query(Customer).filter(Customer.id==check_token.user_id,
                                   Customer.status==1,
                                   or_(Customer.user_type==1,Customer.user_type==2)).first()
    if not user:
        return {"status" : 0, "message": "Accessed only by 'SuperAdmin' or 'Admin' "}
    
    if check_token.status ==1:
        
        filtersalesID=db.query(Sales).filter(Sales.id==sales_id).first()
        
        if filtersalesID.order_status==0:
            
            if update_status==1:
                filtersalesID.order_status=update_status
                db.commit()

                return {"status" : 1, "message" : "Order is confirmed"}
            
            elif update_status==2:
                return {"status" : 0, "message" : "Invalied Order Status"}
            else:
                return {"Status":"Invalide update Status code"}

        elif filtersalesID.order_status==1:
            
            if update_status==1:

                return {"status" : 0, "message" : "Invalied Order Status"}
            
            elif update_status==2:
                filtersalesID.order_status=update_status
                db.commit()
                return {"status" : 2, "message" : "Your Order is Shipped"}
            
            else:
                return {"Status":"Invalide update Status code"}
            
        elif filtersalesID.order_status==2:
            
            if update_status==1:

                return {"status" : 0, "message" : "Invalied Order Status"}
            
            elif update_status==3:
                filtersalesID.order_status=update_status
                db.commit()
                return {"status" : 3, "message" : "Your Order is successfully delivered"}
            
            else:
                return {"Status":"Invalide update Status code"}

        else:
            return {"status" : 0 ,"message":  "Invalied Order Update Status"}         


            
    else:
        return {"message":"Token ID is not Activate"} 
    



    