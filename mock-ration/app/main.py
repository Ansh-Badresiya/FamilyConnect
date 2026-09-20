import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI(
    title="Mock Ration Card Household Service",
    description="⚠️ HACKATHON DEMO ONLY — All household records are synthetic fictional data. No real Ration Card records are used.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).parent.parent / "data" / "households.json"

# Index by person_reference and ration_card_number
_households: list = []
_by_ration_card: dict = {}
_by_person_ref: dict = {}


@app.on_event("startup")
def load_data():
    global _households, _by_ration_card, _by_person_ref
    with open(DATA_PATH) as f:
        _households = json.load(f)

    for hh in _households:
        _by_ration_card[hh["ration_card_number"]] = hh
        for member in hh["members"]:
            _by_person_ref[member["person_reference"]] = hh

    print(f"✅ Loaded {len(_households)} synthetic household records.")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Mock Ration Card Household Service",
        "disclaimer": "HACKATHON DEMO — Synthetic data only. No real Ration Card records.",
        "total_households": len(_households)
    }


@app.get("/api/v1/households/by-person/{person_reference}")
def get_household_by_person(person_reference: str):
    """
    Lookup the household a person belongs to using their person_reference.
    
    ⚠️ This is a HACKATHON DEMO service using entirely synthetic data.
    No real Ration Card or household data is used.
    """
    household = _by_person_ref.get(person_reference)

    if not household:
        return {
            "found": False,
            "message": f"No household found for person reference: {person_reference}"
        }

    # Build member list (strip internal NOTE fields)
    members = [
        {
            "person_reference": m["person_reference"],
            "name": m["name"],
            "date_of_birth": m["date_of_birth"],
            "relationship": m["relationship"]
        }
        for m in household["members"]
    ]

    return {
        "found": True,
        "ration_card_number": household["ration_card_number"],
        "state": household["state"],
        "category": household["category"],
        "annual_income": household["annual_income"],
        "address": household["address"],
        "members": members
    }


@app.get("/api/v1/households/by-ration-card/{ration_card_number}")
def get_household_by_ration_card(ration_card_number: str):
    """
    Lookup a household by ration card number.
    """
    household = _by_ration_card.get(ration_card_number)

    if not household:
        return {
            "found": False,
            "message": f"No household found for ration card: {ration_card_number}"
        }

    members = [
        {
            "person_reference": m["person_reference"],
            "name": m["name"],
            "date_of_birth": m["date_of_birth"],
            "relationship": m["relationship"]
        }
        for m in household["members"]
    ]

    return {
        "found": True,
        "ration_card_number": household["ration_card_number"],
        "state": household["state"],
        "category": household["category"],
        "annual_income": household["annual_income"],
        "address": household["address"],
        "members": members
    }
