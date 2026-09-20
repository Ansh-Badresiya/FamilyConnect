from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApplicationBase(BaseModel):
    family_id: int
    scheme_id: int

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdateStatus(BaseModel):
    status: str
    remarks: Optional[str] = None

class ApplicationResponse(ApplicationBase):
    id: int
    applicant_person_id: int
    status: str
    remarks: Optional[str] = None
    submitted_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True
