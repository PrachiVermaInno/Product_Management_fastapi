from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    category: str
    price: int
    company: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        orm_mode = True
