from fastapi import FastAPI
from app.database import Base, engine
#from app.models import company, category, product
from app.routers import company_routers,category_routers,product_routers
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Product Management API!"}
app.include_router(company_routers.router)
app.include_router(category_routers.router) 
print("hello")
#app.include_router(product_routers.router)