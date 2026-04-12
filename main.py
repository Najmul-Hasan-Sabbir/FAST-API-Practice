from fastapi import FastAPI   
from models import Product
app = FastAPI()   # Note the parentheses ()

@app.get("/")

def greet():
    return "Welcome to FAST API"




products = [
    Product(id=1, name="iPhone 15", description="Latest Apple flagship phone", price=79999, quantity=15),
    Product(id=2, name="Samsung Galaxy S24", description="Android powerhouse with AI features", price=74999, quantity=12),
    Product(id=3, name="MacBook Air M3", description="Thin and light laptop with 18hr battery", price=114999, quantity=8),
    Product(id=4, name="Dell XPS 15", description="Windows premium laptop for developers", price=159999, quantity=5),
    Product(id=5, name="Sony WH-1000XM5", description="Noise cancelling headphones", price=26999, quantity=20),
    Product(id=6, name="Logitech MX Master 3S", description="Ergonomic wireless mouse", price=8999, quantity=25),
    Product(id=7, name="Keychron K3 Pro", description="Mechanical keyboard low profile", price=11999, quantity=10),
    Product(id=8, name="iPad Air", description="M2 chip tablet for productivity", price=54999, quantity=7),
    Product(id=9, name="Samsung 980 Pro SSD", description="1TB NVMe Gen4 storage", price=8999, quantity=30),
    Product(id=10, name="Raspberry Pi 5", description="Single board computer 8GB RAM", price=4999, quantity=18)
]

@app.get("/products")
def all_products():



    # DB connection 
    # Query 
    return products





#using the if condition  
# so for wrong input or random id that is not present in our product list , we will not crash our server 

@app.get("/products/{id}")
def get_product_by_ID(id: int):
    if id < 1 or id > len(products):
        return {"error": f"Product with ID {id} not found"}
    return products[id-1]



@app.post("/products")
def add_product(Product:Product):
    products.append(Product)
    return Product




@app.put("/products")
def update_product(id:int, Product:Product):
    for i in range(len(products)):
        if products[i].id==id:
            products[i]=Product
            return "Product added successfully"


        return "No product found"    





@app.delete("/products")
def delete_product(id:int):
    for i in range (len(products)):
        if products[i].id==id:
            del products[i]
            return "Product Deleted"

    return "Product Not found"       

       