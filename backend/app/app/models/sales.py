from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from database.base_class import Base
# from ..database.base_class import Base



class Sales(Base):
    __tablename__='sales'
    id = Column(Integer,primary_key=True)
    customer_id=Column(Integer,ForeignKey('customer.id'))
    address=Column(String(70))
    postal_code=Column(Integer)
    total_amount=Column(Float)
    payment_type=Column(String(50))
    date=Column(DateTime)
    status=Column(TINYINT,comment=" '1:Active', '-1:Inactive', '0:Delete' ")
    order_status=Column(TINYINT,comment=" '0:Waiting', '1:Confirmed','2:Shipped', '3:Delivered' ")
    
    customer=relationship('Customer', back_populates='sales')
    # product=relationship('Product',back_populates="sales")

    salesdetails=relationship('Salesdetails',back_populates='sales')
    
