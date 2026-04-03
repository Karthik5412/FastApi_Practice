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
        
        
        return {'total' : len(result) ,'items' : result }
    else :
        return {'total' : len(items) ,'items' : items }
    
    
@app.get('/products/top')
def top_products(limit : int = Query(default= 3, ge= 1, le= 15, 
                                    description= 'Select Count'),
                name : str = Query(default= None,max_length= 35, min_length= 3, 
                                    description= 'Search item by name'),
                sort_oder : str = Query(default= 'asc', description= 'Select order')):
    
    
    if not name :
        return products[: limit]
    
    else :
        target = name.lower()
        items = [p for p in products if target in p.get('name','').lower()]
        
        ordered = sorted(items, key= lambda x : x.get('price'), reverse= sort_oder=='desc' )
        
        return ordered[: limit]



@app.get('/products/offset')
def offset_deciding(name : str = Query(default= None, min_length=3, max_length= 15, description= 'Item name' ),
            page_len : int = Query(default= 2, ge= 0, le= 10, description= 'Offsets want to be decide'),
            sort_order : str = Query(default= 'asc', description= 'Specify order'),
            page_no : int = Query(default= 0, ge= 0, le= 100, description= 'Select page no.')) :
    
    if not name : 
        return products[:page_len]
    
    else :
        target = name.strip().lower()
        items = [i for i in products if target in i.get('name','').lower()]
        
        ordered = sorted(items, key= lambda x : x.get('price'), reverse= sort_order == 'desc')
        
        return ordered[page_no :page_len + page_no]
    
    
    
    
    