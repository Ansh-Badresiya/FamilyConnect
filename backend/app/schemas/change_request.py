from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChangeRequestCreate(BaseModel):
    person_id: Optional[int] = None # If null, it's a family field
    field_name: str
    requested_value: str
    reason: Optional[str] = None
    supporting_document: Optional[str] = None

class ChangeRequestResponse(BaseModel):
    id: int
    family_id: int
    person_id: Optional[int] = None
    field_name: str
    old_value: Optional[str] = None
    requested_value: str
    reason: Optional[str] = None
    supporting_document: Optional[str] = None
    verification_status: str
    verification_source: Optional[str] = None
    created_at: datetime
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
