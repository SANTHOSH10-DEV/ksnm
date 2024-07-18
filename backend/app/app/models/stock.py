from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from database.base_class import Base
# from ..database.base_class import Base



class Stock(Base):
    __tablename__='stock'
    id=Column(Integer, primary_key=True)
    product_id=Column(Integer, ForeignKey('product.id'))
    quantity=Column(Integer)
    initial_qty=Column(Integer)
    update_date=Column(Date)
    date=Column(Date)
    status=Column(TINYINT,comment=" '1:Active', '-1:Inactive', '0:Delete' ")
    
    
    product=relationship('Product', back_populates='stock')

    
    