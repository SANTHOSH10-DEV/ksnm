from sqlalchemy import Column, Integer, String,ForeignKey,DateTime
from database.base_class import Base
# from ..database.base_class import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT


class Customer(Base):
    __tablename__='customer'
    id=Column(Integer, primary_key=True)
    first_name=Column(String(30))
    last_name=Column(String(30))
    full_name=Column(String(45),unique=True)
    phone_number=Column(String(12),unique=True)
    email_id=Column(String(50))
    password=Column(String(100))
    status=Column(TINYINT,comment=" '1:Active', '-1:Inactive', '0:Delete' ")
    created_at=Column(DateTime)
    user_type =Column(TINYINT,comment="1->SuperAdmin,2->Admin,3->Employee,4->customer")

    
    sales=relationship('Sales',back_populates='customer')
    api_tokens=relationship('ApiTokens',back_populates='customer')
    wishlist=relationship("Wishlist",back_populates='customer')
    cart=relationship("Cart",back_populates='customer')



#  alembic revision --autogenerate -m "Salesdetails table create"
#  alembic upgrade head