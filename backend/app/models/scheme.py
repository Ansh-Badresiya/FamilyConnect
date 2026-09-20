from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    required_documents = Column(String, nullable=True) # Comma separated list of documents
    is_active = Column(Boolean, default=True)
    
    rules = relationship("SchemeRule", back_populates="scheme", cascade="all, delete-orphan")

class SchemeRule(Base):
    __tablename__ = "scheme_rules"

    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False, index=True)
    description = Column(String, nullable=False) # Human readable rule description e.g. "Annual income must be below 2,00,000"
    
    # Target entity: 'FAMILY' or 'MEMBER'
    target = Column(String, nullable=False)
    
    # JSON based rule configuration
    # Example: {"field": "annual_income", "operator": "<", "value": 200000}
    # Example: {"field": "occupation", "operator": "==", "value": "Student"}
    rule_config = Column(JSON, nullable=False)
    
    scheme = relationship("Scheme", back_populates="rules")
