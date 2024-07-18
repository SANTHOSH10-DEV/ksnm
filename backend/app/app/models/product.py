from sqlalchemy import Column, Integer, String, ForeignKey,Float,Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from database.base_class import Base
# from ..database.base_class import Base



class Product(Base):
    __tablename__='product'
    id=Column(Integer, primary_key=True)
    name=Column(String(45))
    pro_type=Column(Integer, ForeignKey('producttype.id'))
    rate=Column(Float)
    date=Column(Date)
    status=Column(TINYINT,comment=" '1:Active', '-1:Inactive', '0:Delete' ")

    producttype=relationship('Producttype', back_populates='product')
    stock=relationship("Stock",back_populates='product')
    # sales=relationship("Sales",back_populates="product")
    wishlist=relationship('Wishlist', back_populates='product')
    cart=relationship('Cart', back_populates='product')

    salesdetails=relationship("Salesdetails", back_populates="product")

