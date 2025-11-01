from sqlalchemy import Column, Integer, String, Text
from app.config.database import Base

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"
