from pydantic import BaseModel

class CreateSalesdetails(BaseModel):
    
    sales_id : int
    # product_id : int
    # quantity :int
    # rate : int
    # total : int