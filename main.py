from fastapi import FastAPI, Depends
from products_class import Product
from database import session, engine
import db_model 
from sqlalchemy.orm import Session

app = FastAPI()
db_model.base.metadata.create_all(engine)

def get_db() :
    db = session()
    
    try :
        yield db
        
    finally :
        db.close()

@app.get('/')
def greet() :
    return 'My First FastApi Program'

products = [
    Product(id=1, name='Smartphone', describ='Mobile Device', price=25000.0),
    Product(id=2, name='Laptop', describ='Portable Computer', price=55000.0),
    Product(id=3, name='Water Bottle', describ='Stainless Steel Bottle', price=1200.0),
    Product(id=4, name='Backpack', describ='Travel Bag', price=2500.0),
    Product(id=5, name='Ballpoint Pen', describ='Writing Instrument', price=50.0),
    Product(id=6, name='Mechanical Keyboard', describ='External Peripherals', price=4500.0),
    Product(id=7, name='Wireless Mouse', describ='Optical Mouse', price=1500.0),
    Product(id=8, name='Notebook', describ='Hardbound Diary', price=400.0),
    Product(id=9, name='Desk Lamp', describ='LED Study Light', price=1800.0),
    Product(id=10, name='Coffee Mug', describ='Ceramic Cup', price=600.0)
]

@app.get('/products')
def all_products(db : Session = Depends(get_db)) :
    # db = session()
    items = db.query(db_model.dbms).all()
    
    return items

@app.get('/product/{id}')
def product(id : int, db : Session = Depends(get_db) ) :
    
    item = db.query(db_model.dbms).filter(db_model.dbms.id == id).first()
    
    if item:
        return item
    
    else :
        return 'There is no Id for it'
    
    
@app.post('/product')
def add_product(product : Product, db : Session = Depends(get_db)) :
    
    db.add(db_model.dbms(**product.model_dump()))
    db.commit()
    
    items = db.query(db_model.dbms).all()
    
    return items

@app.put('/product') 
def update_product(id : int, product : Product, db : Session = Depends(get_db)) :
    item =db.query(db_model.dbms).filter(db_model.dbms.id == id).first()
    
    if item :
        item.name = product.name
        item.price = product.price
        item.describ = product.describ
    else :
        db.add(db_model.dbms(**product.model_dump()))
    
    db.commit()
    
    return db.query(db_model.dbms).filter(db_model.dbms.id == id).first()
    
@app.delete('/product')
def deleting_product(id : int, db : Session = Depends(get_db)) :
    
    item = db.query(db_model.dbms).filter(db_model.dbms.id == id).first()
    
    if item :
        db.delete(item)
        db.commit()
        return 'Product Deleted Successfully'
    
    else :
        return 'No Such Id'
        
        
        
def db_initialize() :
    
    db = session()
    
    for product in products :
        
        count = db.query(db_model.dbms).count
        
        if count == 0 :
            db.add(db_model.dbms(**product.model_dump()))
            
            db.commit()
        
db_initialize()