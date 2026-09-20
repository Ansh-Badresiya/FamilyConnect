import uuid
import random
import string
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.api import deps
from app.models.user import User
from app.models.family import Family
from app.models.person import Person
from app.models.family_membership import FamilyMembership
from app.services.family_resolver import FamilyResolver
from app.schemas.family import FamilyCreate, FamilyUpdate, FamilyResponse, FamilyWithMembersResponse, FamilyMembershipCreate, FamilyMembershipResponse, PersonUpdate, PersonResponse

router = APIRouter()

def generate_family_id():
    chars = string.ascii_uppercase + string.digits
    random_str = ''.join(random.choices(chars, k=8))
    return f"GJ-FAM-{random_str}"

@router.post("", response_model=FamilyResponse)
def create_family(
    family_in: FamilyCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Check if the user is a citizen and already belongs to a family
    if current_user.role != "CITIZEN":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if current_user.person_id:
        existing_membership = db.query(FamilyMembership).filter(
            FamilyMembership.person_id == current_user.person_id,
            FamilyMembership.status == "ACTIVE"
        ).first()
        if existing_membership:
            raise HTTPException(status_code=400, detail="User already belongs to an active family")

    family_id_str = generate_family_id()
    family = Family(
        **family_in.dict(),
        family_id=family_id_str
    )
    db.add(family)
    db.commit()
    db.refresh(family)

    from datetime import date
    person = Person(
        name=current_user.email.split("@")[0],
        date_of_birth=date(1990, 1, 1),
        gender="Unknown"
    )
    db.add(person)
    db.commit()
    db.refresh(person)

    current_user.person_id = person.id
    db.commit()
    
    membership = FamilyMembership(
        family_id=family.id,
        person_id=person.id,
        relationship="HEAD",
        is_head=True
    )
    db.add(membership)
    
    family.family_head_person_id = person.id
    db.commit()
    db.refresh(family)

    return family

@router.post("/resolve", response_model=FamilyResponse)
def resolve_family(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role != "CITIZEN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return FamilyResolver.resolve_family_for_user(current_user, db)

@router.get("/me", response_model=FamilyWithMembersResponse)
def get_my_family(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if not current_user.person_id:
        raise HTTPException(status_code=404, detail="User is not linked to any person")

    membership = db.query(FamilyMembership).filter(
        FamilyMembership.person_id == current_user.person_id,
        FamilyMembership.status == "ACTIVE"
    ).first()

    if not membership:
        raise HTTPException(status_code=404, detail="User does not belong to any family")

    family = db.query(Family).filter(Family.id == membership.family_id).first()
    memberships = db.query(FamilyMembership).filter(FamilyMembership.family_id == family.id).all()
    
    # attach members
    for mem in memberships:
        mem.person = db.query(Person).filter(Person.id == mem.person_id).first()
    
    family.members = memberships
    return family

@router.post("/{family_id}/members", response_model=FamilyMembershipResponse)
def add_family_member(
    family_id: int,
    member_in: FamilyMembershipCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Create person
    person = Person(**member_in.person.dict())
    db.add(person)
    db.commit()
    db.refresh(person)

    membership = FamilyMembership(
        family_id=family_id,
        person_id=person.id,
        relationship=member_in.relationship,
        is_head=member_in.is_head,
        status=member_in.status
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    
    # Update family head if needed
    if member_in.is_head:
        family = db.query(Family).filter(Family.id == family_id).first()
        if family:
            family.family_head_person_id = person.id
            db.commit()

    membership.person = person
    return membership

@router.put("/{family_id}", response_model=FamilyResponse)
def update_family(
    family_id: int,
    family_in: FamilyUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    raise HTTPException(
        status_code=403, 
        detail="Family details are government-verified and cannot be edited directly. Please submit a Change Request."
    )

@router.put("/persons/{person_id}", response_model=PersonResponse)
def update_person(
    person_id: int,
    person_in: PersonUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
        
    update_data = person_in.dict(exclude_unset=True)
    
    # Block verified fields
    verified_fields = ["name", "gender", "date_of_birth"]
    for field in verified_fields:
        if field in update_data and update_data[field] is not None:
            raise HTTPException(
                status_code=403, 
                detail=f"Field '{field}' is government-verified and cannot be edited directly. Please submit a Change Request."
            )
            
    for key, value in update_data.items():
        if value is not None:
            setattr(person, key, value)
            
    db.commit()
    db.refresh(person)
    return person
