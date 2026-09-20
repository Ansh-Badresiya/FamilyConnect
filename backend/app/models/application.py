from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False, index=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False, index=True)
    applicant_person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    
    # Statuses: SUBMITTED, UNDER_REVIEW, APPROVED, REJECTED
    status = Column(String, default="SUBMITTED", nullable=False)
    remarks = Column(Text, nullable=True)
    
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    family = relationship("Family")
    scheme = relationship("Scheme")
    applicant = relationship("Person")
