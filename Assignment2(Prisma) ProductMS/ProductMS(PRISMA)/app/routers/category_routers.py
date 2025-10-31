from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.models.company import Company

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

#  Create category under a company
@router.post("/")
def create_category(name: str, description: str, company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    new_category = Category(name=name, description=description, company_id=company_id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {"message": "Category created", "category": new_category}

#  Get all categories
@router.get("/")
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

# Get categories by company
@router.get("/by_company/{company_id}")
def get_categories_by_company(company_id: int, db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.company_id == company_id).all()
