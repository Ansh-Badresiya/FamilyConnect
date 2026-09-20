import os
import sys
from datetime import date, datetime

# Ensure app is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.person import Person
from app.models.family import Family
from app.models.family_membership import FamilyMembership
from app.models.scheme import Scheme, SchemeRule
from app.models.application import Application
from app.core.security import get_password_hash
from app.api.families import generate_family_id

def seed():
    db = SessionLocal()
    
    # 1. Create Officer
    officer = db.query(User).filter(User.email == "officer@gujarat.gov.in").first()
    if not officer:
        officer = User(
            email="officer@gujarat.gov.in",
            password_hash=get_password_hash("password123"),
            role="OFFICER",
            is_active=True
        )
        db.add(officer)
        print("Created Officer.")

    # 2. Create Citizens and their Persons
    citizens_data = [
        {"email": "rajesh@example.com", "name": "Rajesh Kumar", "dob": date(1980, 5, 15), "gender": "Male", "mobile": "9876543210", "occupation": "Farmer", "education": "10th"},
        {"email": "sunita@example.com", "name": "Sunita Patel", "dob": date(1990, 8, 20), "gender": "Female", "mobile": "9876543211", "occupation": "Homemaker", "education": "12th"},
        {"email": "amit@example.com", "name": "Amit Shah", "dob": date(1975, 1, 10), "gender": "Male", "mobile": "9876543212", "occupation": "Teacher", "education": "Graduate"}
    ]

    for c in citizens_data:
        user = db.query(User).filter(User.email == c["email"]).first()
        if not user:
            person = Person(
                name=c["name"],
                date_of_birth=c["dob"],
                gender=c["gender"],
                mobile=c["mobile"],
                occupation=c["occupation"],
                education=c["education"]
            )
            db.add(person)
            db.commit()
            db.refresh(person)

            user = User(
                email=c["email"],
                password_hash=get_password_hash("password123"),
                role="CITIZEN",
                person_id=person.id,
                is_active=True
            )
            db.add(user)
            print(f"Created Citizen: {c['name']}")

    db.commit()

    # 3. Create Families and Memberships
    rajesh_user = db.query(User).filter(User.email == "rajesh@example.com").first()
    rajesh = db.query(Person).filter(Person.id == rajesh_user.person_id).first()
    
    family1 = db.query(Family).filter(Family.family_head_person_id == rajesh.id).first()
    if not family1:
        family1 = Family(
            family_id=generate_family_id(),
            family_head_person_id=rajesh.id,
            annual_income=150000.0,
            address="123 Main St",
            district="Ahmedabad",
            taluka="City",
            village="Village A"
        )
        db.add(family1)
        db.commit()
        db.refresh(family1)
        
        mem1 = FamilyMembership(family_id=family1.id, person_id=rajesh.id, relationship="HEAD", is_head=True)
        db.add(mem1)
        print("Created Family 1 (Rajesh)")

    # 4. Create Schemes
    schemes_data = [
        {
            "name": "Student Scholarship",
            "description": "₹10,000 per year for students to support their education.",
            "required_documents": "Aadhaar Card, Student ID, Income Certificate",
            "rules": [
                {"description": "Family annual income must be under ₹3,00,000", "target": "FAMILY", "rule_config": {"field": "annual_income", "operator": "<=", "value": 300000}},
                {"description": "Must have a student in the family", "target": "MEMBER", "rule_config": {"field": "occupation", "operator": "==", "value": "Student"}}
            ]
        },
        {
            "name": "Farmer Assistance",
            "description": "₹6,000 per year for families dependent on agriculture.",
            "required_documents": "Aadhaar Card, Land Record, Bank Passbook",
            "rules": [
                {"description": "Must have a farmer in the family", "target": "MEMBER", "rule_config": {"field": "occupation", "operator": "==", "value": "Farmer"}}
            ]
        },
        {
            "name": "Senior Citizen Assistance",
            "description": "₹2,000 per month pension for senior citizens.",
            "required_documents": "Aadhaar Card, Age Proof, Bank Passbook",
            "rules": [
                {"description": "Must have a member aged 60 or above", "target": "MEMBER", "rule_config": {"field": "age", "operator": ">=", "value": 60}}
            ]
        },
        {
            "name": "Housing Assistance",
            "description": "Financial aid for building a pucca house.",
            "required_documents": "Aadhaar Card, Ration Card, Income Certificate",
            "rules": [
                {"description": "Family annual income must be under ₹1,50,000", "target": "FAMILY", "rule_config": {"field": "annual_income", "operator": "<=", "value": 150000}}
            ]
        },
        {
            "name": "Women Welfare Assistance",
            "description": "Special scheme to empower adult women in the household.",
            "required_documents": "Aadhaar Card, Bank Passbook",
            "rules": [
                {"description": "Must have an adult female member", "target": "MEMBER", "rule_config": {"field": "gender", "operator": "==", "value": "F"}},
                {"description": "Member must be 18 or older", "target": "MEMBER", "rule_config": {"field": "age", "operator": ">=", "value": 18}}
            ]
        },
        {
            "name": "Girl Child Education Assistance",
            "description": "Support for girl children's education.",
            "required_documents": "Aadhaar Card, School ID",
            "rules": [
                {"description": "Must have a female student in the family", "target": "MEMBER", "rule_config": {"field": "gender", "operator": "==", "value": "F"}},
                {"description": "Member must be a student", "target": "MEMBER", "rule_config": {"field": "occupation", "operator": "==", "value": "Student"}}
            ]
        },
        {
            "name": "Skill Development Assistance",
            "description": "Free skill training for unemployed youth.",
            "required_documents": "Aadhaar Card, Education Certificate",
            "rules": [
                {"description": "Member must be unemployed", "target": "MEMBER", "rule_config": {"field": "occupation", "operator": "==", "value": "Unemployed"}},
                {"description": "Member must be between 18 and 35", "target": "MEMBER", "rule_config": {"field": "age", "operator": "<=", "value": 35}}
            ]
        },
        {
            "name": "Agriculture Equipment Assistance",
            "description": "Subsidy for purchasing farming equipment.",
            "required_documents": "Aadhaar Card, Farmer Certificate",
            "rules": [
                {"description": "Must have a farmer in the family", "target": "MEMBER", "rule_config": {"field": "occupation", "operator": "==", "value": "Farmer"}},
                {"description": "Family annual income must be under ₹5,00,000", "target": "FAMILY", "rule_config": {"field": "annual_income", "operator": "<=", "value": 500000}}
            ]
        }
    ]

    for s_data in schemes_data:
        scheme = db.query(Scheme).filter(Scheme.name == s_data["name"]).first()
        if not scheme:
            scheme = Scheme(
                name=s_data["name"],
                description=s_data["description"],
                required_documents=s_data["required_documents"],
                is_active=True
            )
            db.add(scheme)
            db.commit()
            db.refresh(scheme)
            
            for r in s_data["rules"]:
                rule = SchemeRule(
                    scheme_id=scheme.id,
                    description=r["description"],
                    target=r["target"],
                    rule_config=r["rule_config"]
                )
                db.add(rule)
            db.commit()
            print(f"Created Scheme: {s_data['name']}")

    db.close()
    print("Seed complete.")

if __name__ == "__main__":
    seed()
