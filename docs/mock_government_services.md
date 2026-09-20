# Mock Government Services

As a hackathon prototype, FamilyConnect operates in a synthetic environment to avoid utilizing real Personally Identifiable Information (PII) or hitting rate-limited production government APIs.

We built two lightweight Python/FastAPI microservices to simulate external data sources.

## 1. Mock Aadhaar Service (Port 8001)
Simulates a national identity database.
- Provides demographic verification (Name, DOB, Gender).
- Validates synthetic 12-digit numbers.

## 2. Mock Ration Service (Port 8002)
Simulates a state-level household database.
- Stores hierarchical household structures (Head of Family, Spouse, Children).
- Simulates external linkage records that our `FamilyResolver` uses to piece together unified Family Profiles.

## Note on Synthetic Data
All seeded data uses fictional names (e.g. "Rajesh Kumar", "Sunita Patel"), fictional identity numbers (e.g. `482719365041`), and fictional scheme configurations to strictly adhere to standard hackathon compliance policies regarding PII.
