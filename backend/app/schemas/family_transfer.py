from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FamilyTransferVerifyTarget(BaseModel):
    spouse_aadhaar: str
    
class FamilyTransferVerifyResponse(BaseModel):
    target_family_id: str
    target_person_name: str
    
class FamilyTransferCreate(BaseModel):
    spouse_aadhaar: str
    reason: str
    person_id: Optional[int] = None
    
class FamilyTransferResponse(BaseModel):
    id: int
    person_id: int
    current_family_id: int
    target_family_id: int
    reason: str
    spouse_aadhaar: Optional[str] = None
    status: str
    remarks: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
