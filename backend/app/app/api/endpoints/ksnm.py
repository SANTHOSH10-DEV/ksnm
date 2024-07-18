from fastapi import HTTPException,Depends, APIRouter,Body,Form
from sqlalchemy import func,desc,or_
from schemas import *
from models import * 
from datetime import datetime,date,time,timedelta
from utils import db_dependency

router=APIRouter()


# #Most sold item fromDate to todate in orderwise 
@router.post('/most_sales_count')
async def count_of_sales(db:db_dependency, token:str,
                         fromdate : date | None = None, todate : date | None = None):
    # ,ApiTokens.customer.user_type!=4

    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()


    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session has expired. Please, Sign-in again Your ID'})

    if not check_token:
        return {"message":"Token ID is not Activate"} 
    
    user=db.query(Customer).filter(Customer.id==check_token.user_id,
                                   Customer.status==1,
                                   or_(Customer.user_type==1,Customer.user_type==2)).first()
    if not user:
        return {"status" : 0, "message": "Accessed only by 'SuperAdmin' or 'Admin' "}
 
    one_day=timedelta(days=1)
    f_date=fromdate
    # f_date=fromdate+one_day
    t_date=todate+one_day
   
    result=[]
        
    page_SalesDetails=(db.query(Salesdetails.product_id,func.sum(Salesdetails.quantity).label("count_of_sales")
                                ).group_by(Salesdetails.product_id
                                           ).filter(Salesdetails.date.between(f_date, t_date)
                                                    ).order_by(desc('count_of_sales')).all() )
    
    if not page_SalesDetails:
        return {"msg" : "Doesn't have a any data"}
   
    for salesdetail, count_of_sales in page_SalesDetails:
        result.append({
            
            "ProductID" : salesdetail,
            "CountOfSales" : count_of_sales

        })
    return result


# # display Highest to lowest amound perchased customer wise fromdate to todate
@router.post('/high_amount')
async def high_amound(db:db_dependency,token : str,
                         fromdate : date | None = None, todate : date | None = None
                         ):
 
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

    
    oneday=timedelta(days=1)
    todate=todate+oneday
    result=[]
        
    user_data_=(db.query(Sales.customer_id,func.sum(Sales.total_amount).label("total_cash")
                        ).filter(Sales.date.between(fromdate, todate)
                                 ).group_by(Sales.customer_id
                                            ).order_by(desc('total_cash')).all() )
    
    # print(user_data_)
    for user, total_cash in user_data_:
        print(user)
        last_date=db.query(Sales.date).filter(Sales.customer_id==user).order_by(desc(Sales.date)).first()
        # print(last_date.Strftime("%Y-%m-%d"))
        # last_date=last_date.date
        # last_date=last_date.date.strftime("%Y-%m-%d")
        result.append({
            
            "CustomerID" : user,
            "Total Purchased amount" : total_cash,
            "Last Purchase Date": last_date.date.strftime("%Y-%m-%d")

        })
    return result
