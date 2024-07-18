from fastapi import HTTPException,Depends, APIRouter,Body
from typing import Annotated
from schemas import *
from models import * 
from database.session import SessionLocal
from sqlalchemy import func
from datetime import datetime,date
from sqlalchemy.orm import Session


from utils import db_dependency


router=APIRouter()



# # list sales details
# @router.get('/list_sales')
# async def listSales(page_no:int,size:int,db:db_dependency):
#     result=[]
#     line_no=(page_no-1)*size
#     SalesDetails=db.query(Sales).offset(line_no).limit(size).all()
#     # all_sales=db.query(Sales).all()
#     # if (len(all_sales)) % size == 0:
#     #     total_page = int((len(all_sales))/size)
#     # else:
#     #     total_page=((len(all_sales))//size+1)
#     # page_details=( "Page_no:", page_no, "Total_page:", 
#     #               total_page,"Total_no_records:", len(all_sales))
#     for SalesDetail in SalesDetails:
#         result.append({
#             "Sales_id": SalesDetail.id,
#             "CustomerId" : SalesDetail.customer_id,
#             "Address" : SalesDetail.address,
#             "Payment" : SalesDetail.payment_type,
#             "TotalAmount": SalesDetail.total_amount,
#             "DateTime" : SalesDetail.date
#         })

#     return result


#from date to todate salesDetails
@router.get('/SalesList')
async def sales_list(db:db_dependency,token : str, page_no : int,size:int,fromdate : date | None = None,todate : date | None = None):
    
    
    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()

    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session has expired. Please, Sign-in again Your ID'})


    
    if not check_token:
        return {"message":"Token ID is not Activate"} 
      
    result=[]
    if fromdate and todate:
        line_no=(page_no-1)*size
        sales_query = db.query(Sales).filter(Sales.date.between(fromdate, todate))
        if not sales_query:
            return {"msg" : "Not sold "}

        SalesDetails=sales_query.offset(line_no).limit(size).all()
        # all_sales=db.query(Sales).all()
        # if (len(all_sales)) % size == 0:
        #     total_page = int((len(all_sales))/size)
        # else:
        #     total_page=((len(all_sales))//size+1)
        # page_details=( "Page_no:", page_no, "Total_page:", 
        #               total_page,"Total_no_records:", len(all_sales))
        for SalesDetail in SalesDetails:
            result.append({
                "Sales_id": SalesDetail.id,
                "CustomerId" : SalesDetail.customer_id,
                "Address" : SalesDetail.address,
                "Payment" : SalesDetail.payment_type,
                "TotalAmount": SalesDetail.total_amount,
                "DateTime" : SalesDetail.date
            })
        return result

    line_no=(page_no-1)*size
    SalesDetails=db.query(Sales).offset(line_no).limit(size).all()
    # all_sales=db.query(Sales).all()
    # if (len(all_sales)) % size == 0:
    #     total_page = int((len(all_sales))/size)
    # else:
    #     total_page=((len(all_sales))//size+1)
    # page_details=( "Page_no:", page_no, "Total_page:", 
    #               total_page,"Total_no_records:", len(all_sales))
    for SalesDetail in SalesDetails:
        result.append({
            "Sales_id": SalesDetail.id,
            "CustomerId" : SalesDetail.customer_id,
            "Address" : SalesDetail.address,
            "Payment" : SalesDetail.payment_type,
            "TotalAmount": SalesDetail.total_amount,
            "DateTime" : SalesDetail.date
        })

    return result
