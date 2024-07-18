from sqlalchemy import Column, Integer, Float, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from database.base_class import Base
# from ..database.base_class import Base




class Cart(Base):
    __tablename__="cart"
    id=Column(Integer, primary_key=True)
    customer_id=Column(Integer,ForeignKey('customer.id'))
    product_id=Column(Integer, ForeignKey('product.id'))
    quantity=Column(Integer)
    rate=Column(Float)
    total=Column(Float)
    date=Column(DateTime)
    status=Column(TINYINT,comment=" '1:Active', '-1:Inactive', '0:Delete' ")


    customer= relationship('Customer', back_populates='cart')
    product=relationship('Product', back_populates='cart')
    
