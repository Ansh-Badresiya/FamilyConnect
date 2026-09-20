from datetime import timedelta, datetime
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.models.person import Person
from app.models.identity_record import IdentityRecord
from app.schemas.token import Token
from app.schemas.user import UserResponse

router = APIRouter()

class AadhaarLogin(BaseModel):
    aadhaar_number: str

@router.post("/login-aadhaar", response_model=Token)
def login_aadhaar(payload: AadhaarLogin, db: Session = Depends(deps.get_db)):
    if not payload.aadhaar_number:
        raise HTTPException(status_code=400, detail="Aadhaar number is required")
    
    # Verify Aadhaar
    try:
        resp = httpx.post(
            f"{settings.AADHAAR_SERVICE_URL}/api/v1/identity/verify",
            json={"government_id": payload.aadhaar_number},
            timeout=10.0
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to identity service: {str(e)}")
        
    if not data.get("verified"):
        raise HTTPException(status_code=400, detail="Identity could not be verified")
        
    person_ref = data.get("person_reference")
    
    # Check if person already exists (might have been created via family resolver earlier)
    person = db.query(Person).filter(Person.person_reference == person_ref).first()
    
    if not person:
        # Create new person
        dob_str = data.get("date_of_birth")
        dob_obj = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
        
        person = Person(
            person_reference=person_ref,
            name=data.get("name"),
            date_of_birth=dob_obj,
            gender=data.get("gender")
        )
        db.add(person)
        db.commit()
        db.refresh(person)
    else:
        # If person existed but had 'U' gender (from ration stub), update it
        if person.gender == 'U' or person.gender == 'Unknown':
            person.gender = data.get("gender", "U")
            # We can also sync name/dob just in case
            if data.get("name"): person.name = data.get("name")
            dob_str = data.get("date_of_birth")
            if dob_str: person.date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()
            db.commit()
            db.refresh(person)
        
    # Check identity record
    ident = db.query(IdentityRecord).filter(IdentityRecord.provider_person_reference == person_ref).first()
    if not ident:
        ident = IdentityRecord(
            person_id=person.id,
            provider="aadhaar",
            provider_person_reference=person_ref,
            verification_status="VERIFIED"
        )
        db.add(ident)
        db.commit()
    
    # Create or fetch User
    dummy_email = f"{person_ref}@familyconnect.gov.in"
    user = db.query(User).filter(User.person_id == person.id).first()
    
    if not user:
        user = User(
            email=dummy_email,
            password_hash=security.get_password_hash("dummy"),
            role="CITIZEN",
            person_id=person.id
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserResponse)
def get_user_me(current_user: User = Depends(deps.get_current_user)):
    return current_user
