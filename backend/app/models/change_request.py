from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class ChangeRequest(Base):
    __tablename__ = "change_requests"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=True, index=True) # Null if it's a family field
    
    field_name = Column(String, nullable=False)
    old_value = Column(String, nullable=True)
    requested_value = Column(String, nullable=False)
    
    reason = Column(Text, nullable=True)
    supporting_document = Column(String, nullable=True) # URL or reference
    
    # Status: PENDING, AUTO_VERIFIED, MANUAL_REVIEW, APPROVED, REJECTED
    verification_status = Column(String, default="PENDING", nullable=False)
    verification_source = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    family = relationship("Family")
    person = relationship("Person")
