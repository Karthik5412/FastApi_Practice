from fastapi import FastAPI, Query
import json
with open('data.json', 'r') as file :
    products = json.load(file)
    

app = FastAPI()



@app.get('/')
def root():
    return products

@app.get('/product/{id}')
def get_product(id : int):
    
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