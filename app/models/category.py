from sqlalchemy import Column, Integer, String, Text
from app.config.database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
