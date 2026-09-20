from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.models.user import User
from app.models.family import Family
from app.models.person import Person
from app.models.family_membership import FamilyMembership
from app.models.change_request import ChangeRequest
from app.schemas.change_request import ChangeRequestCreate, ChangeRequestResponse

router = APIRouter()

@router.post("", response_model=ChangeRequestResponse)
def create_change_request(
    req: ChangeRequestCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Get active family
    membership = db.query(FamilyMembership).filter(
        FamilyMembership.person_id == current_user.person_id,
        FamilyMembership.status == "ACTIVE"
    ).first()
    
    if not membership:
        raise HTTPException(status_code=400, detail="User is not part of any family")
        
    family_id = membership.family_id
    
    # Get old value
    old_value = None
    
    if req.field_name == "ADD_MEMBER":
        # Adding a member, no old value, person_id should be null
        pass
    elif req.field_name == "REMOVE_MEMBER":
        if not req.person_id:
            raise HTTPException(status_code=400, detail="person_id is required for REMOVE_MEMBER")
        
        pm = db.query(FamilyMembership).filter(
            FamilyMembership.person_id == req.person_id,
            FamilyMembership.family_id == family_id
        ).first()
        
        if not pm:
            raise HTTPException(status_code=403, detail="Person is not in your family")
            
        person = db.query(Person).filter(Person.id == req.person_id).first()
        old_value = person.name
        
    elif req.person_id:
        # It's a person field
        # Ensure person is in the same family
        pm = db.query(FamilyMembership).filter(
            FamilyMembership.person_id == req.person_id,
            FamilyMembership.family_id == family_id
        ).first()
        
        if not pm:
            raise HTTPException(status_code=403, detail="Person is not in your family")
            
        person = db.query(Person).filter(Person.id == req.person_id).first()
        if not person:
            raise HTTPException(status_code=404, detail="Person not found")
            
        if hasattr(person, req.field_name):
            val = getattr(person, req.field_name)
            old_value = str(val) if val is not None else None
        else:
            raise HTTPException(status_code=400, detail=f"Invalid field {req.field_name} for Person")
            
    else:
        # It's a family field
        if req.field_name == "family_id":
            raise HTTPException(status_code=400, detail="Family ID cannot be changed")
            
        family = db.query(Family).filter(Family.id == family_id).first()
        if hasattr(family, req.field_name):
            val = getattr(family, req.field_name)
            old_value = str(val) if val is not None else None
        else:
            raise HTTPException(status_code=400, detail=f"Invalid field {req.field_name} for Family")

    cr = ChangeRequest(
        family_id=family_id,
        person_id=req.person_id,
        field_name=req.field_name,
        old_value=old_value,
        requested_value=req.requested_value,
        reason=req.reason,
        supporting_document=req.supporting_document,
        verification_status="MANUAL_REVIEW" # Hackathon stub: auto review logic can be extended
    )
    
    db.add(cr)
    db.commit()
    db.refresh(cr)
    
    return cr

@router.get("", response_model=List[ChangeRequestResponse])
def get_change_requests(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    membership = db.query(FamilyMembership).filter(
        FamilyMembership.person_id == current_user.person_id,
        FamilyMembership.status == "ACTIVE"
    ).first()
    
    if not membership:
        return []
        
    requests = db.query(ChangeRequest).filter(
        ChangeRequest.family_id == membership.family_id
    ).order_by(ChangeRequest.created_at.desc()).all()
    
    return requests
