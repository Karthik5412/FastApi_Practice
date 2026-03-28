from pydantic import BaseModel

class Product(BaseModel) :
    id : int
    name : str
    describ : str
    price : float
    
    
