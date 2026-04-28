from pydantic import BaseModel, Field, AnyUrl, EmailStr, field_validator, model_validator, computed_field
from uuid import UUID
from typing import Annotated, Optional, List

# "dimensions": 
class dimension_of_product(BaseModel) :
    weight : Annotated[float, Field(le= 25, ge= 5, default= 5)]
    height : Annotated[float, Field(le= 2, ge= 0.2, default= 0.5)]
    depth : Annotated[float, Field(le= 50, ge= 5, default= 10)]

#  seller_data
class seller_model(BaseModel):
    seller_name : Annotated[str,Field(min_length=7,max_length= 25, default='John Doe')]
    seller_rating : Annotated[float, Field(lt= 5, gt= 0, default= None)]
    is_verified : Annotated[bool, Field(default= None, strict= True)]


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
    
    # "dimensions"
    dimensions : dimension_of_product
    
    # "tags"
    tags : Annotated[
        Optional[List[str]],
        Field(title= 'Tags', default= None, max_length= 10, description='Category of product')
    ]
    
    # "manufacturer_email"
    manufacturer_email : Annotated[EmailStr, Field(examples=['johdoe@gmail.com'])]
    
    # "rating": 
    rating : Annotated[
        float,
        Field(default=2.25, lt=5, gt=0, description='Rate about the product')
    ]
    
    # "warehouse_location"
    warehouse_location : Annotated[
        str,
        Field(max_length= 5, min_length=3, examples=["WA-01"])
    ]
    
    # "shipping_code"
    shipping_code : Annotated[
        str,
        Field(max_length= 50, min_length=15, examples=["SHP-WA-01-c552d4e8-128f-4609-ae06-42310fd7b35c"])
    ]
    
    #"quantity_available"
    quantity_available : Annotated[
        int,
        Field(ge=0, description='Quantity of product')
    ]
    
    #"discount"
    discount : Annotated[
        float,
        Field(default=5, le=50, ge=0, description='Available Discount')
    ]
    
    
    # "seller_data"
    seller_data : seller_model
    
    
    # Field validation
    @field_validator('sku', mode='after')
    @classmethod
    def sku_validation(cls, val: str):
        if '-' not in val:
            raise ValueError('Need to put "-"')
        
        if not (len(val.split('-')[-1]) == 3 and  val.split('-')[-1].isnumeric()) :
            raise ValueError('Ending three must end up like this "-124"')
        
        return val
    
    @field_validator('warehouse_location', mode='after')
    @classmethod
    def warehouse_validation(cls, val: str):
        if '-' not in val:
            raise ValueError('Need to put "-"')
        
        if not (val.split('-')[0].isupper() and  val.split('-')[-1].isdigit()) :
            raise ValueError('Ending three must end up like this "KD-12"')
        
        return val
    
    @model_validator(mode='after')
    @classmethod
    def validating_shipping(cls, model : product) :
        
        if model.is_in_stock == True and model.quantity_available == 0 :
            raise ValueError('If Stock how quaintity is 0')
        
        if not model.warehouse_location in model.shipping_code :
            raise ValueError('This Address is not correct')
        
        return model

    
    @computed_field
    @property
    def final_price(self) -> float :
        return round(self.price * (1 - self.discount/100), 2)


