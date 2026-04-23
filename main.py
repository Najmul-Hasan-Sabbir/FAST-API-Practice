from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
import database_models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# ✅ CORS fix — add this right after app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return {"message": "Welcome to FAST API"}


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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = SessionLocal()
    existing = db.query(database_models.Product).first()
    if existing is None:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    db.close()


init_db()


@app.get("/products")
def all_products(db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()


@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if product is None:
        return {"error": f"Product with ID {id} not found"}
    return product


@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    new_product = database_models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    existing = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if existing is None:
        return {"error": f"Product with ID {id} not found"}
    existing.name = product.name
    existing.description = product.description
    existing.price = product.price
    existing.quantity = product.quantity
    db.commit()
    db.refresh(existing)
    return existing


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    existing = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if existing is None:
        return {"error": f"Product with ID {id} not found"}
    db.delete(existing)
    db.commit()
    return {"message": f"Product with ID {id} deleted successfully"}