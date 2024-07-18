from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from database.base_class import Base
# from ..database.base_class import Base



class Salesdetails(Base):
    __tablename__="salesdetails"
    id=Column(Integer, primary_key=True)
    sales_id=Column(Integer,ForeignKey('sales.id'))
    product_id=Column(Integer, ForeignKey('product.id'))
    quantity=Column(Integer)
    rate=Column(Integer)
    total=Column(Integer)
    date=Column(DateTime)
    status=Column(TINYINT,comment=" '1:Active', '-1:Inactive', '0:Delete' ")


    sales= relationship('Sales', back_populates='salesdetails')
    product=relationship('Product', back_populates='salesdetails')


