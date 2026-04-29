from fastapi import FastAPI, Query, Path, HTTPException, Body
import json
from product_schema import product, product_update
from uuid import uuid4, UUID
from curd import all_products, add_product, remove_product, change_product

app = FastAPI()


@app.get('/')
def root():
    return all_products()

@app.get('/product/{id}')
def get_product(id : int):
    products = all_products()
    item = [pro for pro in products if pro.get('id') == id]
    
    return item

@app.get('/products')
def get_by_name(
    name : str = Query(
        default= None, 
        min_length=3, 
        max_length= 10, 
        description= 'Search By Name'
        ), 
    sort_activation : bool = Query(default=False, description= 'For activating Sorting'),
    sort_by_price : str = Query(default= 'asc', description='Order by price'),
    sort_by_name : str = Query(default= 'asc', description='Order by name'),
    limit : int = Query(default= 10, ge=2, le=15, description= 'No. of items you need'),
    offset : int = Query(default= 0, description= 'Page No.')
) :
    
    products = all_products()
    
    if name:
        name = name.lower().strip()
        items = [p for p in products if name in p.get('product_name','').lower()]
    else :
        items = products    
    
    if sort_activation :
        if sort_by_price :
            rev = sort_by_price == 'desc'
            
            items = sorted(items, key= lambda i : i.get('price', 0), reverse=rev)
        
        if sort_by_name :
            rev = sort_by_name == 'desc'
            
            items = sorted(items, key= lambda i : i.get('product_name').lower(), reverse=rev)
        
    start_point = offset * limit
    items = items[start_point: limit + start_point]
    
    return {'Total Items' : len(items), 'Products' : items }


@app.get('/products/{tag}')
def get_by_tag(tag : str = Path(..., examples=["office"], description='Search by category')) :
    
    products = all_products()
    items = []
    tag = tag.strip().lower()
    for p in products :
        if tag in list(p.get('tags','')):
            items.append(p)
    return items

@app.post('/products/')
def create_product(item : product) :
    item_dict = item.model_dump(mode='json')
    item_dict['id'] = str(uuid4())
    
    try :
        add_product(item_dict)
        
    except ValueError:
        raise HTTPException(status_code=404)
    
    return item.model_dump(mode='json')


@app.delete('/products/{product_id}')
def delete_product(product_id : UUID) :
    
    try :
        response = remove_product(str(product_id))
        return response
    
    except Exception as e:
        raise HTTPException(status_code= 404)
    
@app.put('/product/{item_id}')
def update_product(item_id : UUID = Path(...), data : product_update = Body(...) ) :
    try :
        
        updated = change_product(item_id, data.model_dump(mode= 'json', exclude_unset=True))
        
        return updated
    except ValueError as e:
        raise HTTPException(status_code= 404, detail= str(e))