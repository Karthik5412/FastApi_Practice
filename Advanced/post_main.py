from fastapi import FastAPI, Query
import json
from schema import Product


app = FastAPI()

with open('data.json', 'r') as f :
    data = json.load(f)
    
@app.get('/')
def homepage():
    return data

@app.get('/product')
def product_by_name(name : str = Query(default= None,min_length= 3, max_length=20, description= 'Enter name of the product')) :
    
    target = name.strip().lower()
    items = [p for p in data if target in p.get('product_name').lower()]
    
    return items

@app.post('/product', status_code= 201)
def add_products(product : Product) :
    return product