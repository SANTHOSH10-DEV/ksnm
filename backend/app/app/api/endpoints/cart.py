from fastapi import HTTPException, APIRouter,Form,Body, Depends, Query
from schemas import *
from models import * 
from datetime import datetime
from typing import Annotated
# from sqlalchemy.orm import Session

from utils import db_dependency

router=APIRouter()

# cartList  Addcart
@router.post("/add_to_cart")
async def add_cart(token:str,product_id: int , Quantity: Annotated[int, Query(ge=1)], db: db_dependency):
    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()

    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session has expired. Please, Sign-in again Your ID'})


    if not check_token:
        return {"msg" : "Invalied Token ID"}
    

    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session is expired'})


    product_data=db.query(Product).filter(Product.id==product_id,Product.status==1).first()
    cart_list = []
    already_exist=db.query(Cart).filter(Cart.customer_id==check_token.user_id,
                                            Cart.product_id==product_id,
                                            Cart.status==1).first()
    if already_exist:
        return {"message": "This product is already exist your CartList"}

    add_cart = Cart(customer_id=check_token.user_id,product_id=product_id,
                        quantity=Quantity,rate=product_data.rate,
                        total=Cart.rate*Cart.quantity,date=datetime.now(),status=1)
        
    db.add(add_cart)
    
    db.commit()
    
    single_user=db.query(Cart).filter(Cart.customer_id==check_token.user_id,Cart.status==1).all()
    
    return single_user

@router.get("/listcart")
async def list_cart(token : str, db: db_dependency, page_no :int=1, size: int=10):
    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()

    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session has expired. Please, Sign-in again Your ID'})


    if not check_token:
        return HTTPException(status_code=400, detail="Token ID is not activated")
   

    result=[]


    user_cart=db.query(Cart).filter(Cart.customer_id==check_token.user_id,Cart.status==1).all()

    if (len(user_cart)) % size == 0:
        total_page = int((len(user_cart))/size)
    else:
        total_page=((len(user_cart))//size+1)
    
    if total_page < page_no:
        return {"message" : f"Only {total_page} pages available" }

    line_no=(page_no-1)*size
    page_data=db.query(Cart).filter(Cart.customer_id==check_token.user_id,Cart.status==1).offset(line_no).limit(size).all()

    result = [
        {
            "Product Id": cart.product_id,
            "Quantity": cart.quantity,
            "Total": cart.total
        }
        for cart in page_data
    ]
    
    return result

# delete cart item
@router.post("/deletecart")
async def delete_cart(token : str, db: db_dependency,product_id: int):
    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()

    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session has expired. Please, Sign-in again Your ID'})


    if not check_token:
        return HTTPException(status_code=400, detail="Token ID is not activated")
    
    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session is expired'})


    result=[]
    user_cart=db.query(Cart).filter(Cart.customer_id==check_token.user_id,
                                    Cart.product_id==product_id,
                                    Cart.status==1).update({"status": 0})
    db.commit()
    return result
     
#update cart list
@router.put("/update_cart")
async def update_cart(token:str,db: db_dependency,product_id : int, quantity: Annotated[int, Query(ge=1)]):
    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()

    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session has expired. Please, Sign-in again Your ID'})


    if not check_token:
        return HTTPException(status_code=400, detail="Token ID is not activated")
    
    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session is expired'})


    db_cart=db.query(Cart).filter(Cart.customer_id==check_token.user_id,
                                  Cart.product_id==product_id,
                                  Cart.status==1).first()
    if db_cart:
        db_cart.quantity=quantity
        db_cart.total=db_cart.rate*quantity
        db.commit()
        # db.refresh(db_cart)
        return {"message" : "Updated successfully"}
    return {"message" : "This Product ID doesn't exist your CartList"}

def verify_postal_code(pin_code):
    if len(str(pin_code))==6:
        return True
    else:
        return False

# # cartList purchase
@router.post("/purchased_cart_products")
async def purchase_cart_item(db: db_dependency,token:str,payment: Payment = Form(...),
                             address:str = Form(..., max_length= 80),
                             postal_code: int = Form(...)) :
    check_token=db.query(ApiTokens).filter(ApiTokens.token==token,ApiTokens.status==1).first()


    if check_token.expires_at < datetime.now():
        check_token.status = -1
        db.commit()
        return ({"status": 0, "message" : 'Your session has expired. Please, Sign-in again Your ID'})

    if not verify_postal_code(postal_code):
         raise HTTPException(status_code= 400, detail= "Invalied Postal code")

    if not check_token:
        return HTTPException(status_code=400, detail="Token ID is not activated")
    
    cart_user=db.query(Cart).filter(Cart.customer_id==check_token.user_id,Cart.status==1).all()

    if not cart_user:
         return {"message": "Cart is Empty. Add items in cart"}

    result=[]

    SalesADD=Sales(customer_id=check_token.user_id,address=address,
              postal_code=postal_code,payment_type=payment)
    
    db.add(SalesADD)

    list_item=[]
    for one in cart_user:
        db_sk=db.query(Stock).filter(Stock.product_id==one.product_id).one()

        if not db_sk:
            return {"message":"Product is not found"}

        if db_sk.quantity<one.quantity:
                    raise HTTPException(status_code=400, 
                                        detail= f"product id {db_sk.product_id} only {db_sk.quantity} items availabe" )
    
        if db_sk:
            current_sk=({db_sk.quantity-one.quantity})
       
            db_sk.update_date=datetime.now()
            db_sk.quantity=current_sk
            if current_sk == 0:
                db_sk.status=-1
                db.commit()
        one.status=-1   
        db.commit()

        db_sales=Salesdetails(sales_id=SalesADD.id,product_id=one.product_id,
                              quantity=one.quantity,rate=one.rate,
                              total=one.quantity*one.rate,status=1,
                              date=datetime.now())
        list_item.append(db_sales.total)
        db.add(db_sales)
        db.commit()
        db.refresh(db_sales)
    
    amount=0

    for li in list_item:
         amount += li
    SalesADD.total_amount = amount
    SalesADD.order_status=0
    SalesADD.date=datetime.now()
    SalesADD.status=1
    db.add(SalesADD)
    db.commit()

    result.append(
            {
              "SalesId": SalesADD.id,
              "Address": SalesADD.address,
              "Payment_type": SalesADD.payment_type,
              "Total_Amount": SalesADD.total_amount
                }
            )

    return result
