from fastapi import FastAPI   
from models import Product
app = FastAPI()   # Note the parentheses ()

@app.get("/")

def greet():
    return "Welcome to FAST API"




products=[

Product(id=1, name="mobile", description="Best phone now", price=20000, quantity=5),
Product(id=2, name="Laptop", description="best laptop", price=66000, quantity=2)


]

@app.get("/products")
def all_products():
    return products
