from fastapi import FastAPI, Depends
from models import Product
from db import session, engine, get_db
import db_models
from sqlalchemy.orm import Session

app = FastAPI()

# creates all the database tables defined by any model, using database connection.
db_models.Base.metadata.create_all(bind=engine)

# static products list
products= [
    Product(id=1, name="Laptop", description="14'' laptop in black colour", price=1599.9, quantity=5),
    Product(id=2, name="Mobile", description="iPhone 17 Pro max", price=1200.99, quantity=15)
]

def init_db():
    db = session()

    count = db.query(db_models.Product).count()
    if count == 0:
        for product in products:
            # we are not passing the instances of products as its pydantic type, rather we are converting them into sqlalchemy type from pydantic type, and then converting them into dictionary coz sqlalchemy expect key value pairs, and we are unpacking all the keys values using ** operator.
            db.add(db_models.Product(**product.model_dump()))

        db.commit()

init_db()

# getting home page data
@app.get("/")
def greet():
    return "Hello world"

# getting all the products
@app.get("/products")
def get_all_products(db: Session =  Depends(get_db)):
    # use the session
    db = session()

    # perform actions
    products = db.query(db_models.Product).all()

    return products

# getting single product by id
@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    # for product in products:
    #     if product.id == id:
    #         return product
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if(db_product):
        return db_product
    return "No product found"

# adding product to a list
@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    # products.append(product)
    db_product = db.add(db_models.Product(**product.model_dump()))

    db.commit()
    # return products
    return db_product
    

# update a product with id
@app.put("/product")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    # for i in range(len(products)):
    #     if products[i].id == id:
    #         products[i] = product
    #         return "product updated successfully"
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()

    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated"
    else: 
        return "product not found"

# delete a product by id
@app.delete("/product")
def delete_product(id: int, db: Session = Depends(get_db)):
    # for i in range(len(products)):
    #     if products[i].id == id:
    #         del products[i] # this will delete the whole product at index i
    #         # del product this will only delete the copy while iterating through the list using for product in products: here product is an object and del will only delete the copy of the product not the actual product from the list.
    #         return "product deleted successfully"
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted"
    else:
        return "product not found"
