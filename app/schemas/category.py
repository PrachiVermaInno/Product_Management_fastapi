from pydantic import BaseModel, Field, validator
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Category name (required)")
    description: Optional[str] = Field(None, description="Category description (optional)")
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Category name cannot be empty or whitespace only')
        return v.strip()


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True
