from sqlalchemy import Column, Integer, String,Date
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from database.base_class import Base
# from ..database.base_class import Base


class Producttype(Base):
    __tablename__='producttype'
    id=Column(Integer,primary_key=True)
    name=Column(String(45))
    date=Column(Date)
    status=Column(TINYINT,comment=" '1:Active', '-1:Inactive', '0:Delete' ")

    product=relationship('Product', back_populates='producttype')

 