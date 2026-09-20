from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.api import deps
from app.models.user import User
from app.models.family_membership import FamilyMembership
from app.models.application import Application
from app.models.scheme import Scheme
from pydantic import BaseModel

router = APIRouter()

class ApplicationCreate(BaseModel):
    scheme_id: int

@router.post("")
def create_application(
    req: ApplicationCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    membership = db.query(FamilyMembership).filter(
        FamilyMembership.person_id == current_user.person_id,
        FamilyMembership.status == "ACTIVE"
    ).first()
    
    if not membership:
        raise HTTPException(status_code=400, detail="User is not part of any family")
        
    scheme = db.query(Scheme).filter(Scheme.id == req.scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
        
    # Check if application already exists
    existing = db.query(Application).filter(
        Application.family_id == membership.family_id,
        Application.scheme_id == scheme.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Application already submitted for this scheme")
        
    application = Application(
        family_id=membership.family_id,
        scheme_id=scheme.id,
        applicant_person_id=current_user.person_id,
        status="SUBMITTED"
    )
    
    db.add(application)
    db.commit()
    db.refresh(application)
    
    return application

@router.get("/me")
def get_my_applications(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    membership = db.query(FamilyMembership).filter(
        FamilyMembership.person_id == current_user.person_id,
        FamilyMembership.status == "ACTIVE"
    ).first()
    
    if not membership:
        return []
        
    applications = db.query(Application).filter(
        Application.family_id == membership.family_id
    ).all()
    
    # Eager load scheme info for frontend
    res = []
    for app in applications:
        res.append({
            "id": app.id,
            "status": app.status,
            "remarks": app.remarks,
            "submitted_at": app.submitted_at,
            "scheme": {
                "name": app.scheme.name
            }
        })
    return res
