import json
from product_schema import product
from uuid import uuid4

def all_products():
    with open('dummy.json', 'r') as file :
        products = json.load(file)
    
    return products

def save_product(products : list[dict]) -> None :
    with open('dummy.json', 'w') as f :
        json.dump(products, f, indent= 2)

def add_product(item : dict) -> dict :
    products = all_products()
    
    if any(p['sku'] == item['sku'] for p in products) :
        raise ValueError('This sku is already exist')
    
    products.append(item)
    save_product(products)
    
    return item

def remove_product(item_id : str) :
    products = all_products()
    for idx , p in enumerate(products):
        if p['id'] == item_id :
            deleted = products.pop(idx)
            
            save_product(products)
            return deleted
        
    raise ValueError('No Such Value')
