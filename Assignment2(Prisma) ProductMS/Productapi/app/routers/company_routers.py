from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.company import Company

router = APIRouter(prefix="/companies", tags=["Company"])

#  Create company
@router.post("/companies/")
def create_company(name: str, descriptions: str,db: Session = Depends(get_db)):
    new_company = Company(name=name,description=descriptions)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

# Read all companies
@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    return companies

# 🧩 Read company by ID
@router.get("/{company_id}")
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# 🧩 Update company
@router.put("/{company_id}")
def update_company(company_id: int, name: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    company.name = name
    db.commit()
    db.refresh(company)
    return company

# 🧩 Delete company
@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(company)
    db.commit()
    return {"message": "Company deleted successfully"}
