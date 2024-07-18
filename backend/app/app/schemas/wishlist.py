from pydantic import BaseModel

class AddWishlist(BaseModel):
    # cus_id:str
    pro_id:int
    