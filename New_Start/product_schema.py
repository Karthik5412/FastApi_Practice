from pydantic import BaseModel, Field, AnyUrl, EmailStr
from uuid import UUID
from typing import Annotated, Optional, List

class product(BaseModel):
    
    # "id"
    id : UUID
    
    # "product_name"
    product_name : Annotated[
        str,
        Field(
            title= 'Product name',
            strict= True,
            max_length= 25,
            min_length= 5,
            description= 'Write the name of product',
            examples=['Silent Click Mouse','Noise Cancelling Headphones']
    )]
    
    # "sku": 
    sku : Annotated[
        str,
        Field(
            title= 'sku',
            max_length= 26,
            min_length= 6,
            examples=["HP-NC-99-004"]
    )]
    
    
    # "price"
    price : Annotated[
        float,
        Field(ge=30, title='Price', examples=['1249.99'])
    ]
    
    
    # "is_in_stock"
    is_in_stock : Annotated [
        bool, Field(title= 'In stock', strict= True)
    ]
    
    
    # "dimensions": {
    #   "width": 32.3,
    #   "height": 1.5,
    #   "depth": 40.9
    # },
    
    
    # "tags"
    tags : Annotated[
        Optional[List[str]],
        Field(title= 'Tags', default= None, max_length= 10, description='Category of product')
    ]
    
    # "manufacturer_email"
    manufacturer_email : Annotated[EmailStr, Field(examples=['johdoe@gmail.com'])]
    
    # "rating": 4.7,
    rating : Annotated[
        float,
        Field(default=2.25, lt=5, gt=0, description='Rate about the product')
    ]
    
    # "warehouse_location": "WA-01",
    



