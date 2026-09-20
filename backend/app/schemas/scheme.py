from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SchemeRuleBase(BaseModel):
    field_name: str
    operator: str
    value: str
    logical_group: str = "AND"

class SchemeRuleCreate(SchemeRuleBase):
    pass

class SchemeRuleResponse(SchemeRuleBase):
    id: int
    scheme_id: int
    class Config:
        from_attributes = True

class SchemeBase(BaseModel):
    name: str
    department: str
    description: Optional[str] = None
    benefit_description: Optional[str] = None
    required_documents: Optional[str] = None
    is_active: bool = True

class SchemeCreate(SchemeBase):
    rules: List[SchemeRuleCreate] = []

class SchemeUpdate(SchemeBase):
    name: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None

class SchemeResponse(SchemeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    rules: List[SchemeRuleResponse] = []
    class Config:
        from_attributes = True

class EligibilityResult(BaseModel):
    scheme_id: int
    scheme_name: str
    benefit_description: Optional[str] = None
    required_documents: Optional[str] = None
    eligible: bool
    matched_rules: List[str]
    failed_rules: List[str]
