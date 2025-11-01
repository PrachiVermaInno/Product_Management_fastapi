from pydantic import BaseModel, Field, validator
from typing import Optional


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Company name (required)")
    description: Optional[str] = Field(None, description="Company description (optional)")
    website: Optional[str] = Field(None, description="Company website URL (optional)")
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Name cannot be empty or whitespace only')
        return v.strip()
    
    @validator('website')
    def validate_website(cls, v):
        if v and not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('Website must start with http:// or https://')
        return v


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    website: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    
    class Config:
        from_attributes = True
