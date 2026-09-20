from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.family_membership import FamilyMembership
from app.services.eligibility_engine import EligibilityEngine

router = APIRouter()

@router.get("/my-benefits")
def get_my_benefits(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get all eligible and ineligible schemes for the current user's family.
    """
    # Find the user's active family
    membership = db.query(FamilyMembership).filter(
        FamilyMembership.person_id == current_user.person_id,
        FamilyMembership.status == "ACTIVE"
    ).first()
    
    if not membership:
        raise HTTPException(status_code=400, detail="User is not part of any family")
        
    family_id = membership.family_id
    
    # Run eligibility engine
    results = EligibilityEngine.evaluate_all_schemes(db, family_id)
    
    return {
        "eligible": [r for r in results if r["eligible"]],
        "not_eligible": [r for r in results if not r["eligible"]]
    }
