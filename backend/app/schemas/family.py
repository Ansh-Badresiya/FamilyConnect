from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class PersonBase(BaseModel):
    name: str
    date_of_birth: date
    gender: str
    mobile: Optional[str] = None
    occupation: Optional[str] = None
    education: Optional[str] = None

class PersonCreate(PersonBase):
    pass

class PersonResponse(PersonBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class FamilyBase(BaseModel):
    annual_income: float
    address: Optional[str] = None
    district: Optional[str] = None
    taluka: Optional[str] = None
    village: Optional[str] = None

class FamilyCreate(FamilyBase):
    pass

class FamilyUpdate(BaseModel):
    annual_income: Optional[float] = None
    address: Optional[str] = None
    district: Optional[str] = None
    taluka: Optional[str] = None
    village: Optional[str] = None

class PersonUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    mobile: Optional[str] = None
    occupation: Optional[str] = None
    education: Optional[str] = None
    date_of_birth: Optional[date] = None

class FamilyResponse(FamilyBase):
    id: int
    family_id: str
    family_head_person_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class FamilyMembershipBase(BaseModel):
    relationship: str
    is_head: bool = False
    status: str = "ACTIVE"

class FamilyMembershipCreate(FamilyMembershipBase):
    person: PersonCreate

class FamilyMembershipResponse(FamilyMembershipBase):
    id: int
    family_id: int
    person_id: int
    joined_at: datetime
    left_at: Optional[datetime] = None
    person: PersonResponse
    class Config:
        from_attributes = True

class FamilyWithMembersResponse(FamilyResponse):
    members: List[FamilyMembershipResponse] = []
