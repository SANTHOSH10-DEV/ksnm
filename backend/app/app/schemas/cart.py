from pydantic import BaseModel
from typing import List


class Listcart(BaseModel):
    pro_id:int
    quantity:int
    # rate:float
    
    

class Addcart(BaseModel):
    # cus_id:int
    products:List[Listcart]


class UpdateCart(Listcart):
    pass

class CartRespose(Listcart):
    pass