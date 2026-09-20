from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.sql import func
from app.db.base_class import Base

class FamilyMembership(Base):
    __tablename__ = "family_memberships"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    relationship = Column(String, nullable=False)
    is_head = Column(Boolean, default=False)
    status = Column(String, default="ACTIVE")
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    left_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index('ix_family_memberships_person_active', 'person_id', unique=True, postgresql_where=(status == 'ACTIVE')),
    )
