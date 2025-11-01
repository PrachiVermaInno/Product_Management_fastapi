from pydantic import BaseModel, Field, validator
from typing import Optional
from app.schemas.company import CompanyResponse


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Product name (required)")
    description: Optional[str] = Field(None, description="Product description (optional)")
    category: str = Field(..., min_length=1, max_length=100, description="Product category (required)")
    price: float = Field(..., gt=0, description="Product price - must be greater than 0")
    company_id: int = Field(..., gt=0, description="Company ID - must be a positive integer")


class ProductCreate(ProductBase):
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return round(v, 2)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    company_id: Optional[int] = Field(None, gt=0)


class ProductResponse(ProductBase):
    id: int
    company: CompanyResponse
    
    class Config:
        from_attributes = True
