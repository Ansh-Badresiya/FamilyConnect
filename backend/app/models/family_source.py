from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base

class FamilySource(Base):
    __tablename__ = "family_sources"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False, index=True)
    source_type = Column(String, nullable=False) # e.g. "ration_card"
    source_reference = Column(String, nullable=False, unique=True, index=True) # e.g. "739258146203"
    verified_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
