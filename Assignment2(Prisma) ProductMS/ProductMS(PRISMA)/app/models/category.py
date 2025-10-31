from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"
    __table__args={'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    company_id=Column(Integer, ForeignKey("companies.id") )
    # One-to-many relationship with Product
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
    
    #relationship to company
    company = relationship("Company", back_populates="categories")