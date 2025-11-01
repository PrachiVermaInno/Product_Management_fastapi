from fastapi import FastAPI, HTTPException, Depends
from app.config.database import engine, Base, SessionLocal,get_db
from app.models import Company, Product, Category
from sqlalchemy.orm import Session
from app.schemas.company import CompanyCreate,CompanyResponse
from app.schemas.product import ProductCreate, ProductResponse
from app.schemas.category import CategoryCreate,CategoryResponse
from app.routes import company_routes,product_routes,categories_routes

# Create all tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

# Initialize FastAPI app
app = FastAPI(
    title="Product Management API",
    description="REST API with PostgreSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
# Include routers
app.include_router(company_routes.router)
app.include_router(product_routes.router)
app.include_router(categories_routes.router)

@app.get("/")
def root():
    return {
        "message": "Product Management API is running!",
        "docs": "/docs",
        "test_endpoints" : "/companies",
        "endpoints": {
            "companies": {
                "list": "GET /companies/",
                "create": "POST /companies/",
                "get": "GET /companies/{id}",
                "update": "PUT /companies/{id}",
                "delete": "DELETE /companies/{id}"
            },
            "products": {
                "list": "GET /products/",
                "create": "POST /products/",
                "search": "GET /products/search",
                "get": "GET /products/{id}",
                "update": "PUT /products/{id}",
                "delete": "DELETE /products/{id}"
            },
            "categories": {
                "list": "GET /categories/",
                "create": "POST /categories/",
                "get": "GET /categories/{id}",
                "update": "PUT /categories/{id}",
                "delete": "DELETE /categories/{id}"
            }
        }
    
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.post("/companies/", response_model=CompanyResponse, status_code=201)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """
    Create a new company with automatic validation
    """
    # Check if company already exists
    existing = db.query(Company).filter(Company.name == company.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company with this name already exists")
    
    # Create new company
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    return db_company

@app.get("/companies/", response_model=list[CompanyResponse])
def list_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get all companies
    """
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies

# product endpoints

@app.post("/products/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    # Verify company exists
    company = db.query(Company).filter(Company.id == product.company_id).first()
    if not company:
        raise HTTPException(status_code=400, detail=f"Company with ID {product.company_id} not found")
    
    # Create product
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product

@app.get("/products/", response_model=list[ProductResponse])
def list_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all products with nested company details"""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get single product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
    return product

# # ==================== CATEGORY ENDPOINTS ====================

@app.post("/categories/", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category"""
    # Check duplicate
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Category '{category.name}' already exists"
        )
    
    # Create category
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category

@app.get("/categories/", response_model=list[CategoryResponse])
def list_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all categories"""
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

@app.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get single category by ID"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=404, 
            detail=f"Category with ID {category_id} not found"
        )
    return category
