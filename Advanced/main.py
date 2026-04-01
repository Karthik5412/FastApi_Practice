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
                                    description= 'Search item by name')) -> list[dict]:
    target = name.lower()
    
    if name :
        items = [i for i in products if target in i['name'].lower() ] 
        
        return items 
    
    else :
        return [{}]
    