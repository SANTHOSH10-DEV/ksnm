from fastapi import HTTPException,Depends, APIRouter,Body,Form
from schemas import *
from models import * 
# from typing import Annotated
# from database.session import SessionLocal
from datetime import datetime
# from sqlalchemy.orm import Session

from utils import db_dependency


router=APIRouter()


#  salesdetails
@router.post("/SalesDetails")
async def sales_details(db:db_dependency,token : str,sales_id: int = Form(None),
                        product_id : int = Form(None)):
    
    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()
    if not check_token:
        return {"message":"Token ID is not Activate"} 
      
    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session is expired'})

    if sales_id and product_id:
        result=[]
        filtersalesID=db.query(Salesdetails
                               ).filter_by(sales_id=sales_id,
                                           status=1,product_id=product_id).all()
        if filtersalesID:
            for eachdetails in filtersalesID:
                result.append({
                    "SalesID" : eachdetails.id,
                    "ProductID" : eachdetails.product_id,
                    "Quantity" : eachdetails.quantity,
                    "Rate" : eachdetails.rate,
                    "Total" : eachdetails.total,
                    "DateTime" : eachdetails.date
                })
            return result
        return {"message" : "Null"}

    elif sales_id:
        result=[]
        filtersalesID=db.query(Salesdetails
                               ).filter_by(sales_id=sales_id).all()
        if filtersalesID:
            for eachdetails in filtersalesID:
                result.append({
                    "SalesID" : eachdetails.id,
                    "ProductID" : eachdetails.product_id,
                    "Quantity" : eachdetails.quantity,
                    "Rate" : eachdetails.rate,
                    "Total" : eachdetails.total,
                    "DateTime" : eachdetails.date
                })

            return result
        return {"message" : "Null"}

    elif product_id:
        result=[]
        filtersalesID = db.query(Salesdetails
                                 ).filter_by(product_id=product_id).all()
        if filtersalesID:
            for eachdetails in filtersalesID:
                result.append({
                    "SalesID" : eachdetails.id,
                    "ProductID" : eachdetails.product_id,
                    "Quantity" : eachdetails.quantity,
                    "Rate" : eachdetails.rate,
                    "Total" : eachdetails.total,
                    "DateTime" : eachdetails.date
                })
            return result
        return {"message" : "Null"}
    else:
        result=[]
        filtersalesID = db.query(Salesdetails).all()
        if filtersalesID:
            for eachdetails in filtersalesID:
                result.append({
                    "SalesID" : eachdetails.id,
                    "ProductID" : eachdetails.product_id,
                    "Quantity" : eachdetails.quantity,
                    "Rate" : eachdetails.rate,
                    "Total" : eachdetails.total,
                    "DateTime" : eachdetails.date
                })
            return result
        return {"message" : "Null"}


