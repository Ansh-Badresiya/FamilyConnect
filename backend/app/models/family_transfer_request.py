from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class FamilyTransferRequest(Base):
    __tablename__ = "family_transfer_requests"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False, index=True)
    current_family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    target_family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    
    # E.g. marriage, adoption, etc
    reason = Column(String, nullable=False)
    
    # We might need to store the spouse/reference Aadhaar they used to prove the transfer
    spouse_aadhaar = Column(String, nullable=True)
    
    # Status: PENDING, APPROVED, REJECTED
    status = Column(String, default="PENDING", nullable=False)
    remarks = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    person = relationship("Person")
    current_family = relationship("Family", foreign_keys=[current_family_id])
    target_family = relationship("Family", foreign_keys=[target_family_id])
