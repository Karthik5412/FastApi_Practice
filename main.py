from fastapi import FastAPI, Depends
from products_class import Product
from database import session, engine
import db_model 
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8501",  
    "http://127.0.0.1:8501",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

db_model.base.metadata.create_all(engine)

def get_db() :
    db = session()
    
    try :
        yield db
        
    finally :
        db.close()



@app.get('/')
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
    
    return 'Item Added'

@app.put('/product') 
def update_product(id : int, product : Product, db : Session = Depends(get_db)) :
    item =db.query(db_model.dbms).filter(db_model.dbms.id == id).first()
    
    if item :
        item.name = product.name
        item.price = product.price
        item.describ = product.describ
        db.commit()
    
        return 'Successfully Updated'
    else :
        db.add(db_model.dbms(**product.model_dump()))
        db.commit()
    
        return 'Successfully Added'
    
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