from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

base = declarative_base()

class dbms(base) :
    
    __tablename__ = 'Products'
    
    id = Column(Integer, primary_key=True, index= True)
    name = Column(String)
    describ = Column(String)
    price = Column(Float)