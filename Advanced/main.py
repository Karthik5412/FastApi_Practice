from fastapi import FastAPI, Query
import json 

app = FastAPI()

with open('products.json', 'r') as f:
    products = json.load(f)
    
    
@app.get('/')
def homepage():
        return products
    
@app.get('/product/{id}')
def item_by_id (id : int) :
    for i in products:
        if i.get('id') == id :
            return i
    
    return "No such ID"

@app.get('/product')
def search_by_name(name : str = Query(default= None, max_length= 35, min_length= 3, 
                                    description= 'Search item by name'
                                    ),
                    sort_status : bool = Query(default = False, description= 'Sorting'),
                    order : str = Query(default= 'asc', description= 'Specify order')
                    ):
    target = name.lower()
    
    if name :
        items = [i for i in products if target in i['name'].lower() ]  
        
    
    if not items :
        return 'No Such Items'
    
    if sort_status :
        
        reverse = order == 'desc'
        
        
        result = sorted(items, key= lambda x : x.get('price',0), reverse=reverse)
        
        
        return result 
    