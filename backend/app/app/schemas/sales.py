from pydantic import BaseModel
from enum import Enum


class Payment(str, Enum):
    phone_pay = "Phone_pay"
    google_pay = "Google_pay"
    paytm = " Paytm"
    cash = "Cash"

# class CreateSales(BaseModel):
    
    # # customer_id : int
    # address: str
    # postal_code : int
    # # total_amount : float
    # payment_type : Payment