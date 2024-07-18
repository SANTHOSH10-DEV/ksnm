from fastapi import HTTPException, APIRouter,Body, Depends
from sqlalchemy import or_
from schemas import *
from models import * 
from datetime import datetime


from utils import db_dependency

router=APIRouter()



# add new product in stock table
@router.post("/NewProductStock")
async def new_product_stock(token:str,product_id:int, initial_quantity:int, db:db_dependency):

    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()
    if not check_token:
        
        return {"message":"Token ID is not Activate"} 

    
    user=db.query(Customer).filter(Customer.id==check_token.user_id,
                                   Customer.status==1,
                                   or_(Customer.user_type==1,Customer.user_type==2)).first()
    if not user:
        return {"status" : 0, "message": "Accessed only by 'SuperAdmin' or 'Admin' "}
    

    db_sk=db.query(Product).filter(Product.id==product_id).one()
    if not db_sk:
        return {"message":"Product is not found"  }

    db_stock=Stock(product_id = product_id,
                   quantity = initial_quantity,
                   initial_qty = initial_quantity,
                   status=1,date=datetime.now())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

# update product_quantity in stock table
@router.put("/update_stock")
async def update_stock(token:str,product_id:int,UpdateStockQuantity: int, db:db_dependency):

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
    


    db_sk=db.query(Stock).filter(Stock.product_id==product_id).one()
    if not db_sk:
        return {"message":"Product is not found"}
    else:
        current_sk=({db_sk.quantity + UpdateStockQuantity})
       
        db_sk.update_date=datetime.now()
        db_sk.quantity=current_sk
        # if current_sk <=0:
        #     db_sk.status=0


        db.commit()
        db.refresh(db_sk)
        return db_sk

# @router.get("/ListStock")
# async def list_stock( db:db_dependency):
#     db_stock=db.query(Stock).all()
#     result=[]
#     for SingleProduct in db_stock:
#         result.append({"ProductID": SingleProduct.product_id,
#                    "Quantity": SingleProduct.quantity})
#     return result


@router.get("/ListStock")
async def list_stock( db:db_dependency,token: str,size: int,page_no:int):

    
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

    
    all_stock=db.query(Stock).all()

    if (len(all_stock)) % size == 0:
        total_page = int((len(all_stock))/size)
    else:
        total_page=((len(all_stock))//size+1)

    if total_page < page_no:
        return {"message" : f"Only {total_page} pages available" }

    line_no=(page_no-1)*size
    db_stock=db.query(Stock).offset(line_no).limit(size).all()

    result=[]
    for SingleProduct in db_stock:
        result.append({"StockID":SingleProduct.id,
                       "ProductID": SingleProduct.product_id,
                       "Quantity": SingleProduct.quantity,
                       "Initial Quantity" : SingleProduct.initial_qty
                       })
    return result