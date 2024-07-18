from typing import Union
from pydantic import BaseModel


class CreateProduct(BaseModel):
    name:str
    pro_type:int
    rate:float | None
    
class UpdateProduct(BaseModel):
    name: str | None
    pro_type : int | None
    rate : float | None