import json
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Mock Aadhaar Identity Service",
    description="⚠️ HACKATHON DEMO ONLY — All identities are synthetic fictional data. No real Aadhaar records are used.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load citizen data at startup
DATA_PATH = Path(__file__).parent.parent / "data" / "citizens.json"
_citizens_by_aadhaar: dict = {}

@app.on_event("startup")
def load_data():
    global _citizens_by_aadhaar
    with open(DATA_PATH) as f:
        citizens = json.load(f)
    _citizens_by_aadhaar = {c["aadhaar_number"]: c for c in citizens}
    print(f"✅ Loaded {len(_citizens_by_aadhaar)} synthetic citizen records.")


class VerifyRequest(BaseModel):
    government_id: str


class VerifyResponse(BaseModel):
    verified: bool
    aadhaar_number: Optional[str] = None
    person_reference: Optional[str] = None
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    message: Optional[str] = None


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Mock Aadhaar Identity Service",
        "disclaimer": "HACKATHON DEMO — Synthetic data only. No real Aadhaar records.",
        "total_records": len(_citizens_by_aadhaar)
    }


@app.post("/api/v1/identity/verify", response_model=VerifyResponse)
def verify_identity(request: VerifyRequest):
    """
    Verify a government identity number (mock Aadhaar).
    
    ⚠️ This is a HACKATHON DEMO service using entirely synthetic data.
    No real Aadhaar numbers or personal data are used.
    """
    gov_id = request.government_id.strip()

    # Validate format: must be exactly 12 digits
    if not gov_id.isdigit() or len(gov_id) != 12:
        return VerifyResponse(
            verified=False,
            message="Invalid format. Government ID must be exactly 12 numeric digits."
        )

    citizen = _citizens_by_aadhaar.get(gov_id)
    if not citizen:
        return VerifyResponse(
            verified=False,
            message="Identity could not be verified. ID not found in records."
        )

    return VerifyResponse(
        verified=True,
        aadhaar_number=citizen["aadhaar_number"],
        person_reference=citizen["person_reference"],
        name=citizen["name"],
        date_of_birth=citizen["date_of_birth"],
        gender=citizen["gender"]
    )


@app.get("/api/v1/identity/by-reference/{person_reference}")
def get_by_reference(person_reference: str):
    """
    Internal: Lookup citizen by person_reference.
    Used by FamilyConnect to fetch identity details.
    """
    for c in _citizens_by_aadhaar.values():
        if c["person_reference"] == person_reference:
            return {
                "found": True,
                "person_reference": c["person_reference"],
                "name": c["name"],
                "date_of_birth": c["date_of_birth"],
                "gender": c["gender"]
            }
    return {"found": False, "message": "Person reference not found"}
