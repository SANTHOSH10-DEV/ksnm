
from pydantic import BaseModel

class CreateCustomer(BaseModel):
    first_name:str
    last_name:str|None
    full_name: str
    phone_number:str
    email_id:str
    password:str

class UserResponse(BaseModel):
    full_name: str
    phone_number:str
    email_id:str

class UpdateUser(BaseModel):
    first_name:str |None
    last_name:str|None
    full_name: str|None
    phone_number:str|None
    email_id:str|None
    password:str|None
