from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base_class import Base

class IdentityRecord(Base):
    __tablename__ = "identity_records"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False, index=True)
    provider = Column(String, nullable=False) # e.g. "aadhaar"
    provider_person_reference = Column(String, nullable=False, unique=True, index=True)
    verification_status = Column(String, nullable=False, default="VERIFIED")
    verified_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
