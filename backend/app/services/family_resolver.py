import httpx
import uuid
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.models.person import Person
from app.models.family import Family
from app.models.family_membership import FamilyMembership
from app.models.family_source import FamilySource
from app.models.identity_record import IdentityRecord

class FamilyResolver:
    @staticmethod
    def resolve_family_for_user(user: User, db: Session):
        if not user.person_id:
            raise HTTPException(status_code=400, detail="User is not linked to a verified identity.")
            
        person = db.query(Person).filter(Person.id == user.person_id).first()
        if not person or not person.person_reference:
            raise HTTPException(status_code=400, detail="Verified identity details missing.")
            
        person_ref = person.person_reference
        
        # Check if already in a family
        existing_membership = db.query(FamilyMembership).filter(FamilyMembership.person_id == person.id).first()
        if existing_membership:
            return db.query(Family).filter(Family.id == existing_membership.family_id).first()
            
        # Call Mock Ration Service
        try:
            resp = httpx.get(
                f"{settings.RATION_SERVICE_URL}/api/v1/households/by-person/{person_ref}",
                timeout=10.0
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to communicate with Ration service: {str(e)}")
            
        if not data.get("found"):
            raise HTTPException(status_code=404, detail="NO_HOUSEHOLD_FOUND: Could not find household in government records.")
            
        ration_card = data.get("ration_card_number")
        
        # Check if family source already exists
        family_source = db.query(FamilySource).filter(FamilySource.source_reference == ration_card).first()
        if family_source:
            # Family was already created by another member!
            family = db.query(Family).filter(Family.id == family_source.family_id).first()
            # In theory, FamilyMembership should already exist for this person because 
            # the first person to resolve created stubs for everyone.
            # But just in case, we check and add it if missing.
            membership = db.query(FamilyMembership).filter(
                FamilyMembership.family_id == family.id,
                FamilyMembership.person_id == person.id
            ).first()
            if not membership:
                # Find relationship from data
                rel = "MEMBER"
                for m in data.get("members", []):
                    if m.get("person_reference") == person_ref:
                        rel = m.get("relationship")
                        break
                membership = FamilyMembership(family_id=family.id, person_id=person.id, relationship=rel)
                db.add(membership)
                db.commit()
            return family
            
        # Creating a NEW Family
        family_id_str = f"GJ-FAM-{str(uuid.uuid4().hex[:6]).upper()}"
        family = Family(
            family_id=family_id_str,
            annual_income=data.get("annual_income", 0.0),
            address=data.get("address", {}).get("village", ""),
            district=data.get("address", {}).get("district", ""),
            taluka=data.get("address", {}).get("taluka", ""),
            village=data.get("address", {}).get("village", ""),
            status="ACTIVE"
        )
        db.add(family)
        db.commit()
        db.refresh(family)
        
        # Create FamilySource
        fs = FamilySource(
            family_id=family.id,
            source_type="ration_card",
            source_reference=ration_card
        )
        db.add(fs)
        
        # Process all members
        head_person_id = None
        for m_data in data.get("members", []):
            m_ref = m_data.get("person_reference")
            m_rel = m_data.get("relationship")
            
            # Check if person stub already exists
            m_person = db.query(Person).filter(Person.person_reference == m_ref).first()
            if not m_person:
                dob_str = m_data.get("date_of_birth")
                dob_obj = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
                # Try to fetch true gender from Mock Aadhaar
                member_gender = "U"
                try:
                    aadhaar_resp = httpx.get(
                        f"{settings.AADHAAR_SERVICE_URL}/api/v1/identity/by-reference/{m_ref}",
                        timeout=5.0
                    )
                    if aadhaar_resp.status_code == 200:
                        aadhaar_data = aadhaar_resp.json()
                        if aadhaar_data.get("found"):
                            member_gender = aadhaar_data.get("gender", "U")
                except Exception:
                    pass
                
                m_person = Person(
                    person_reference=m_ref,
                    name=m_data.get("name"),
                    date_of_birth=dob_obj,
                    gender=member_gender
                )
                db.add(m_person)
                db.commit()
                db.refresh(m_person)
            else:
                # Data mismatch check for DOB
                dob_str = m_data.get("date_of_birth")
                dob_obj = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
                if m_person.date_of_birth and dob_obj and m_person.date_of_birth != dob_obj:
                    # PROMPT: "DATA_MISMATCH: Dob differs"
                    raise HTTPException(
                        status_code=409, 
                        detail=f"DATA_MISMATCH: Date of birth for member {m_person.name} differs between Identity and Household records."
                    )
                
            if m_rel == "HEAD":
                head_person_id = m_person.id
                
            # Create FamilyMembership
            fm = FamilyMembership(
                family_id=family.id,
                person_id=m_person.id,
                relationship=m_rel,
                is_head=(m_rel == "HEAD")
            )
            db.add(fm)
            
        if head_person_id:
            family.family_head_person_id = head_person_id
            
        db.commit()
        db.refresh(family)
        return family
