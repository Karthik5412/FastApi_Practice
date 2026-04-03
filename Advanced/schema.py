from pydantic import BaseModel, Field, AnyUrl
from typing import Annotated, Optional, List

class Product(BaseModel) :
    id : Annotated[int, Field (
        gt=0,
        description= 'Enter Product id'
        )]
    
    product_name: Annotated[str, Field (min_length= 3, max_length= 20, title='Product', description= 'Enter Product name ')]
    
    sku: Annotated[str, Field (min_length= 6, max_length= 30,title='SKU', description= 'Stock keeping unit', examples= ["LP-PRO-14-001"])]
    
    price : Annotated[float, Field (default= 10, strict= True, description= 'Enter Price')]
    
    is_in_stock : Annotated[bool,Field(description= 'Is available ?')]
    
    # "dimensions": { "width": 32.3, "height": 1.5 },
    tags: Annotated[ Optional[List[str]], Field(default= None, max_length= 5, description= 'Atleast one tag')]
    
    manufacturer_email : Annotated[AnyUrl, Field(description= 'Enter Mail') ]
    
    rating: Annotated[float, Field (title= 'Rating',strict= True, gt= 0, le= 10, description= 'Rate product with in 10')]
    
    warehouse_location: Annotated[str, Field (min_length= 4, max_length= 10,title='Location', description= 'Warehouse Location', examples= ["WA-01"])]