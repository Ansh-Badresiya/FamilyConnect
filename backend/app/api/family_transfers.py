import httpx
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.core.config import settings
from app.models.user import User
from app.models.family import Family
from app.models.person import Person
from app.models.family_membership import FamilyMembership
from app.models.family_source import FamilySource
from app.models.family_transfer_request import FamilyTransferRequest
from app.schemas.family_transfer import FamilyTransferCreate, FamilyTransferResponse, FamilyTransferVerifyTarget, FamilyTransferVerifyResponse
from app.services.family_resolver import FamilyResolver

router = APIRouter()

def _verify_spouse_aadhaar_and_get_family(spouse_aadhaar: str, db: Session):
    # Verify Aadhaar
    try:
        resp = httpx.post(
            f"{settings.AADHAAR_SERVICE_URL}/api/v1/identity/verify",
            json={"government_id": spouse_aadhaar},
            timeout=10.0
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to identity service: {str(e)}")
        
    if not data.get("verified"):
        raise HTTPException(status_code=400, detail="Identity could not be verified")
        
    person_ref = data.get("person_reference")
    spouse_name = data.get("name")
    
    # We create a dummy User so we can leverage the existing FamilyResolver
    dummy_user = User(role="CITIZEN", person_id=None)
    
    # Check if person already exists
    person = db.query(Person).filter(Person.person_reference == person_ref).first()
    if not person:
        # Create person stub
        dob_str = data.get("date_of_birth")
        dob_obj = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
        
        person = Person(
            person_reference=person_ref,
            name=spouse_name,
            date_of_birth=dob_obj,
            gender=data.get("gender")
        )
        db.add(person)
        db.commit()
        db.refresh(person)
        
    dummy_user.person_id = person.id
    
    # Try resolving family using standard FamilyResolver
    try:
        target_family = FamilyResolver.resolve_family_for_user(dummy_user, db)
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=f"Could not resolve target family: {e.detail}")
        
    return target_family, spouse_name

@router.post("/verify-target", response_model=FamilyTransferVerifyResponse)
def verify_target(
    req: FamilyTransferVerifyTarget,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    target_family, spouse_name = _verify_spouse_aadhaar_and_get_family(req.spouse_aadhaar, db)
    
    return {
        "target_family_id": target_family.family_id,
        "target_person_name": spouse_name
    }

@router.post("", response_model=FamilyTransferResponse)
def create_transfer_request(
    req: FamilyTransferCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    target_person_id = req.person_id if req.person_id else current_user.person_id
    
    # 1. Get current active membership
    current_membership = db.query(FamilyMembership).filter(
        FamilyMembership.person_id == target_person_id,
        FamilyMembership.status == "ACTIVE"
    ).first()
    
    if not current_membership:
        raise HTTPException(status_code=400, detail="User does not have an active family membership")
        
    # Verify they have permission if they are transferring someone else
    if req.person_id and req.person_id != current_user.person_id:
        # Check if current_user is in the same family as the target person
        user_membership = db.query(FamilyMembership).filter(
            FamilyMembership.person_id == current_user.person_id,
            FamilyMembership.family_id == current_membership.family_id,
            FamilyMembership.status == "ACTIVE"
        ).first()
        if not user_membership:
            raise HTTPException(status_code=403, detail="You do not have permission to transfer this person")
        
    # 2. Verify target
    target_family, _ = _verify_spouse_aadhaar_and_get_family(req.spouse_aadhaar, db)
    
    if target_family.id == current_membership.family_id:
        raise HTTPException(status_code=400, detail="Target family is the same as current family")
        
    # 3. Create Transfer Request
    transfer = FamilyTransferRequest(
        person_id=target_person_id,
        current_family_id=current_membership.family_id,
        target_family_id=target_family.id,
        reason=req.reason,
        spouse_aadhaar=req.spouse_aadhaar,
        status="APPROVED", # Hackathon MVP auto-approve
        remarks="Auto-approved via Aadhaar + Ration DB Integration",
        completed_at=datetime.utcnow()
    )
    db.add(transfer)
    
    # 4. Perform Transfer (Transaction)
    # Deactivate old
    current_membership.status = "INACTIVE"
    current_membership.left_at = func.now()
    
    # Create new ACTIVE membership
    new_membership = FamilyMembership(
        family_id=target_family.id,
        person_id=target_person_id,
        relationship="MEMBER", # Ideally determined dynamically or asked
        is_head=False,
        status="ACTIVE"
    )
    db.add(new_membership)
    db.commit()
    db.refresh(transfer)
    
    return transfer

@router.get("", response_model=List[FamilyTransferResponse])
def get_transfers(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    transfers = db.query(FamilyTransferRequest).filter(
        FamilyTransferRequest.person_id == current_user.person_id
    ).order_by(FamilyTransferRequest.created_at.desc()).all()
    
    return transfers
