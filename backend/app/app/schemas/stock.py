from pydantic import BaseModel


class CreateStock(BaseModel):
    
    pro_id: int
    # qty: int
    initial_qty: int
    
    
class UpdateStock(BaseModel):
    pro_id:int | None
    qty:int | None
    