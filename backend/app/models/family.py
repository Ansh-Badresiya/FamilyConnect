from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.db.base_class import Base

class Family(Base):
    __tablename__ = "families"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(String, unique=True, index=True, nullable=False)
    family_head_person_id = Column(Integer, nullable=True)
    annual_income = Column(Float, nullable=False, default=0.0)
    address = Column(String, nullable=True)
    district = Column(String, nullable=True)
    taluka = Column(String, nullable=True)
    village = Column(String, nullable=True)
    status = Column(String, nullable=False, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
