# FamilyConnect Gujarat — Hackathon MVP

You are building a hackathon MVP for the problem statement:

> **Introduction of Family ID in Gujarat to improve beneficiary management for various government schemes.**

## CORE IDEA

Build a government-style citizen platform where a citizen can register using a **mock Aadhaar/government identity service**. After successful identity verification, the system retrieves household information from a **mock Ration Card service** and automatically creates or links the citizen to a **Family ID**.

The normal flow must require **no government officer intervention**.

The system should automatically:

```text
Citizen
   ↓
Identity Verification
   ↓
Household/Ration Card Lookup
   ↓
Family Resolution
   ↓
Create OR Link Family ID
   ↓
Unified Family Profile
   ↓
Scheme Eligibility Engine
   ↓
Eligible Government Schemes
   ↓
Application
   ↓
Application Tracking
```

Use mock government data/services because this is a hackathon prototype.

---

# IMPORTANT DEVELOPMENT RULES

1. This is a **time-constrained hackathon project**.
2. Build a small, polished, fully working MVP.
3. Do NOT overengineer.
4. Use a modular monolith for FamilyConnect.
5. Mock Aadhaar and Ration Card services should behave like external government APIs.
6. **Never use real Aadhaar or real Ration Card data.**
7. All government identifiers and datasets must be synthetic/mock data created only for the hackathon.
8. Mock Aadhaar numbers should **look like real Aadhaar numbers**: exactly 12 numeric digits.
9. Mock Ration Card numbers should use a **realistic numeric government-ID style**, without copying real records.
10. Use internal person references such as `PERSON-10001` for communication between mock services.
11. Do not store raw Aadhaar numbers as the primary identity in FamilyConnect.
12. The system must automatically resolve normal cases.
13. Human/officer intervention should only exist as an optional future exception-resolution mechanism.
14. Do not build AI/ML in the initial MVP.
15. Complete and test each phase before moving to the next.
16. Never break previously working functionality while implementing a new phase.
17. Keep the application runnable after every phase.
18. Clearly display **"Hackathon Demo / Synthetic Data"** somewhere in the UI so users know the government identifiers are not real.

---

# TECHNOLOGY STACK

## Main Application

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* React Router
* Axios
* Recharts

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Alembic
* JWT
* bcrypt/passlib or equivalent secure password hashing

### Database

* PostgreSQL

### Infrastructure

* Docker
* Docker Compose

---

# SYSTEM ARCHITECTURE

Use this architecture:

```text
                         CITIZEN
                            │
                            ▼
                   React Frontend
                            │
                            ▼
                    FamilyConnect API
                        FastAPI
                            │
          ┌─────────────────┼──────────────────┐
          │                 │                  │
          ▼                 ▼                  ▼
    Identity Adapter   Family Service     Scheme Service
          │                 │                  │
          │                 ▼                  ▼
          │          Family Resolver     Eligibility Engine
          │
          │
    ┌─────┴─────────┐
    │               │
    ▼               ▼
Mock Aadhaar    Mock Ration
   Service        Service
    │               │
    ▼               ▼
Aadhaar DB       Ration DB

                            │
                            ▼
                    Application Service
                            │
                            ▼
                       PostgreSQL
```

---

# SERVICE SEPARATION

Create three logical applications:

```text
familyconnect/
│
├── backend/              # Main FamilyConnect application
├── frontend/             # React application
├── mock-aadhaar/         # Mock government identity service
├── mock-ration/          # Mock government household service
├── docs/
└── docker-compose.yml
```

The mock services must communicate with FamilyConnect using HTTP APIs.

**Do NOT directly access the mock service databases from FamilyConnect.**

This is important because we want to demonstrate real external-system integration.

---

# PHASE 0 — REPOSITORY INSPECTION & PROJECT SETUP

Before writing code:

1. Inspect the repository.
2. Determine whether an existing frontend/backend exists.
3. Reuse useful code if present.
4. Do not blindly overwrite existing files.
5. Create a clear implementation plan.
6. Create the required project structure.

Target structure:

```text
familyconnect/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── api/
│   │   ├── services/
│   │   └── integrations/
│   ├── alembic/
│   ├── tests/
│   ├── seed.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── types/
│   │   └── App.tsx
│   ├── Dockerfile
│   └── package.json
│
├── mock-aadhaar/
│   ├── app/
│   ├── data/
│   ├── Dockerfile
│   └── requirements.txt
│
├── mock-ration/
│   ├── app/
│   ├── data/
│   ├── Dockerfile
│   └── requirements.txt
│
├── docs/
├── docker-compose.yml
├── .env.example
└── README.md
```

At the end of Phase 0:

* Project structure exists.
* Docker Compose is configured.
* All services can start.
* README contains basic setup instructions.

---

# PHASE 1 — MOCK AADHAAR GOVERNMENT SERVICE

Build a standalone mock Aadhaar service.

This service represents an external government identity provider.

## Requirements

Create approximately **20–30 fictional citizens**.

Every mock Aadhaar number must:

* contain exactly 12 digits
* contain numbers only
* look like a normal Aadhaar-format identifier
* be completely synthetic
* not belong to any real person
* not be generated from actual Aadhaar data

Example synthetic Aadhaar numbers:

```text
482719365041
617384920156
835261749302
294817563920
751936284105
```

Use an internal reference separately:

```text
PERSON-10001
PERSON-10002
PERSON-10003
```

Example record:

```text
Aadhaar Number: 482719365041
Person Reference: PERSON-10001
Name: Rajesh Patel
DOB: 1975-03-12
Gender: M
```

Another:

```text
Aadhaar Number: 617384920156
Person Reference: PERSON-10002
Name: Meena Patel
DOB: 1978-08-21
Gender: F
```

Another:

```text
Aadhaar Number: 835261749302
Person Reference: PERSON-10003
Name: Rahul Patel
DOB: 2004-07-15
Gender: M
```

**Important:** Never use real Aadhaar numbers. These numbers are only synthetic examples for the hackathon.

## API

Create:

```text
POST /api/v1/identity/verify
```

Request:

```json
{
  "government_id": "835261749302"
}
```

Response:

```json
{
  "verified": true,
  "aadhaar_number": "835261749302",
  "person_reference": "PERSON-10003",
  "name": "Rahul Patel",
  "date_of_birth": "2004-07-15",
  "gender": "M"
}
```

For invalid IDs:

```json
{
  "verified": false,
  "message": "Identity could not be verified"
}
```

Add health endpoint:

```text
GET /health
```

Test the service independently.

---

# PHASE 2 — MOCK RATION CARD SERVICE

Build another standalone external mock government service.

This represents the household/ration-card database.

Create **10–15 fictional households**.

Ration Card numbers should look like realistic numeric government identifiers while remaining completely synthetic.

Example:

```text
739258146203
581426937105
864219573048
315792684201
927461835029
```

Do not use real ration-card numbers.

Example household:

```text
Ration Card Number: 739258146203

Members:

PERSON-10001 → Rajesh Patel → HEAD
PERSON-10002 → Meena Patel → SPOUSE
PERSON-10003 → Rahul Patel → SON
PERSON-10004 → Priya Patel → DAUGHTER
```

Important:

The ration service should connect household members to the same `person_reference` used by the mock Aadhaar service.

## API

Create:

```text
GET /api/v1/households/by-person/{person_reference}
```

Response:

```json
{
  "found": true,
  "ration_card_number": "739258146203",
  "members": [
    {
      "person_reference": "PERSON-10001",
      "relationship": "HEAD"
    },
    {
      "person_reference": "PERSON-10002",
      "relationship": "SPOUSE"
    },
    {
      "person_reference": "PERSON-10003",
      "relationship": "SON"
    },
    {
      "person_reference": "PERSON-10004",
      "relationship": "DAUGHTER"
    }
  ],
  "address": {
    "district": "Surendranagar",
    "taluka": "Wadhwan",
    "village": "Demo Village"
  }
}
```

Also implement:

```text
GET /health
```

Create test cases for:

* Existing household
* Person not found
* Household with multiple members

---

# PHASE 3 — FAMILYCONNECT DATABASE

Now build the main FamilyConnect database.

Use PostgreSQL + SQLAlchemy + Alembic.

Create these core tables:

```text
users
persons
identity_records
families
family_memberships
family_sources
schemes
scheme_rules
applications
```

## users

```text
id
email
password_hash
role
person_id
is_active
created_at
updated_at
```

Roles:

```text
CITIZEN
ADMIN
```

`ADMIN` is only for managing demo schemes/data. It is NOT required for normal family creation.

---

## persons

```text
id
person_reference
name
date_of_birth
gender
mobile
occupation
education
created_at
updated_at
```

`person_reference` should correspond to the mock identity provider reference.

Example:

```text
PERSON-10003
```

---

## identity_records

Store information about how the person was verified.

```text
id
person_id
provider
provider_person_reference
verification_status
verified_at
```

Example:

```text
provider = MOCK_AADHAAR
provider_person_reference = PERSON-10003
verification_status = VERIFIED
```

Do not store raw Aadhaar numbers in the main FamilyConnect database.

---

## families

```text
id
family_id
family_head_person_id
annual_income
address
district
taluka
village
status
created_at
updated_at
```

Family ID example:

```text
GJ-FAM-8X29KQ
```

Make `family_id` UNIQUE.

Do not encode personal information into Family ID.

---

## family_memberships

```text
id
family_id
person_id
relationship
is_head
status
joined_at
left_at
```

Status:

```text
ACTIVE
INACTIVE
```

Important business rule:

> A person can have only one ACTIVE family membership at a time.

---

## family_sources

Store where family information came from.

```text
id
family_id
source_type
source_reference
verified_at
```

Example:

```text
source_type = MOCK_RATION_CARD
source_reference = 739258146203
```

This gives us data provenance.

---

# PHASE 4 — AUTHENTICATION

Implement citizen authentication.

Important:

Registration should be based on government identity verification.

Do NOT make the user manually create a person profile first.

Flow:

```text
Register
   ↓
Enter Mock Aadhaar Number
   ↓
Call Mock Aadhaar Service
   ↓
Identity Verified
   ↓
Create Person
   ↓
Create User Account
   ↓
Login
```

For MVP, use:

```text
Email
Password
Aadhaar Number
```

JWT authentication.

Create APIs:

```text
POST /api/auth/register
POST /api/auth/login
GET /api/auth/me
```

Registration should call the Mock Aadhaar API.

If identity verification fails:

```text
Registration blocked
```

---

# PHASE 5 — AUTOMATIC FAMILY RESOLUTION ⭐

This is the most important phase.

Create a dedicated:

```text
FamilyResolver
```

service.

It should perform:

```text
Verified Person
       ↓
Mock Ration Card Lookup
       ↓
Household Found?
       ↓
Find existing Family
       ↓
Create OR Link Family
```

## Case 1 — New Family

Citizen is verified.

Ration card exists:

```text
739258146203
```

No FamilyConnect family exists for that ration-card reference.

Then:

```text
Create Family
     ↓
Generate Family ID
     ↓
Create family membership
     ↓
Store ration source
```

Example:

```text
GJ-FAM-8X29KQ
```

---

## Case 2 — Existing Family

Citizen is verified.

Ration Card:

```text
739258146203
```

already maps to:

```text
GJ-FAM-8X29KQ
```

Then:

```text
DO NOT create another family.

Link person to:

GJ-FAM-8X29KQ
```

---

## Case 3 — Multiple family members register

Rajesh registers:

```text
739258146203 → GJ-FAM-8X29KQ
```

Later Rahul registers:

```text
739258146203 → GJ-FAM-8X29KQ
```

Later Meena registers:

```text
739258146203 → GJ-FAM-8X29KQ
```

All members must resolve to the same Family ID.

This is a critical demo scenario.

---

## Case 4 — Data mismatch

Example:

Mock Aadhaar:

```text
Aadhaar Number: 835261749302
Name: Rahul Patel
DOB: 2004-07-15
```

Mock Ration:

```text
Person Reference: PERSON-10003
Name: Rahul Patel
DOB: 2003-07-15
```

The system should NOT blindly create/link the family.

Return:

```text
VERIFICATION_EXCEPTION
```

Store the exception for future handling.

For MVP, show the citizen:

> "We could not automatically verify your household information. Please resolve the data discrepancy."

Do not build a full officer workflow yet.

---

## Case 5 — No Ration Card

If the citizen is identity-verified but no household is found:

```text
Identity Verified
      ↓
Ration Card Not Found
      ↓
No automatic Family ID
```

Show:

> "Your identity was verified, but no household record was found in the available household data."

For MVP, provide a simple:

```text
Request Family Verification
```

button that creates an exception record.

Do NOT automatically invent a Family ID.

---

# PHASE 6 — FAMILY PROFILE

Create citizen family dashboard.

After login:

```text
Family ID: GJ-FAM-8X29KQ
```

Display:

```text
Family Information
-------------------------
Family ID
Family Head
District
Taluka
Village
Number of Members
Annual Income
Verification Status
Data Sources
```

Members:

```text
Name
Relationship
Age
Gender
Occupation
Education
```

Show data provenance where useful:

```text
Identity → Mock Aadhaar
Household → Mock Ration Card
Family ID → FamilyConnect
```

---

# PHASE 7 — FAMILY ID RESOLUTION API

Create an API such as:

```text
POST /api/families/resolve
```

The endpoint should:

1. Get authenticated citizen.
2. Check verified identity.
3. Call mock Ration API.
4. Resolve household.
5. Find/create FamilyConnect family.
6. Link citizen.
7. Return family information.

Example response:

```json
{
  "status": "RESOLVED",
  "family_id": "GJ-FAM-8X29KQ",
  "members_count": 4,
  "verification_status": "VERIFIED"
}
```

Possible statuses:

```text
CREATED
LINKED
ALREADY_LINKED
VERIFICATION_EXCEPTION
NO_HOUSEHOLD_FOUND
```

---

# PHASE 8 — SCHEME CATALOGUE

Now implement government scheme management.

Create:

```text
schemes
scheme_rules
```

Create approximately 8–10 fictional/demo schemes.

Examples:

```text
Student Scholarship
Farmer Assistance
Housing Assistance
Women Welfare Assistance
Girl Child Education Assistance
Skill Development Assistance
Senior Citizen Assistance
Agriculture Equipment Assistance
Education Support
Rural Housing Assistance
```

Clearly mark them as:

> Demo Scheme Data

Do not present invented rules as actual government scheme rules.

---

# PHASE 9 — ELIGIBILITY ENGINE ⭐

Create a generic rules-based eligibility engine.

It must NOT contain scheme-specific hardcoded logic.

Input:

```text
Family Profile
+
Family Members
+
Scheme Rules
```

Output:

```text
Eligible
OR
Not Eligible
```

And provide explanations.

Example:

```json
{
  "scheme_id": 1,
  "eligible": true,
  "matched_rules": [
    "Annual income is within the configured limit",
    "Student member found",
    "Age requirement satisfied"
  ],
  "failed_rules": []
}
```

For an ineligible scheme:

```json
{
  "scheme_id": 2,
  "eligible": false,
  "matched_rules": [
    "Gujarat location condition satisfied"
  ],
  "failed_rules": [
    "Annual income exceeds configured threshold"
  ]
}
```

Rules should come from the database.

Support:

```text
==
!=
>
>=
<
<=
IN
```

Rules can apply to:

```text
FAMILY
MEMBER
```

---

# PHASE 10 — BENEFIT DISCOVERY

Create a prominent button:

```text
Find Benefits for My Family
```

Flow:

```text
Family Profile
       ↓
Load active schemes
       ↓
Eligibility Engine
       ↓
Evaluate all schemes
       ↓
Eligible / Not Eligible
```

Display:

```text
Potential Benefits

✓ Student Scholarship
✓ Farmer Assistance
✓ Housing Assistance

Not Eligible

✗ Senior Citizen Assistance
```

For each eligible scheme:

```text
Scheme Name
Benefit Description
Why Eligible
Required Documents
Apply
```

This should be one of the main demo features.

---

# PHASE 11 — APPLICATION SYSTEM

Create:

```text
applications
```

Fields:

```text
id
family_id
scheme_id
applicant_person_id
status
remarks
submitted_at
updated_at
```

Statuses:

```text
SUBMITTED
UNDER_REVIEW
APPROVED
REJECTED
```

For the hackathon, simplify document requirements.

Application flow:

```text
Eligible Scheme
      ↓
Apply
      ↓
Application Created
      ↓
SUBMITTED
```

The user should be able to track the application.

---

# PHASE 12 — AUTOMATED APPLICATION PROCESSING

Since the goal is to reduce manual government intervention, keep the application flow automated where possible.

When a citizen applies:

```text
Application
     ↓
Eligibility Engine
     ↓
Eligibility confirmed?
     │
   YES
     ↓
Application moves forward
```

For MVP, the final approval can be simulated/demo-controlled through an admin endpoint.

Do not claim that this represents actual government approval processes.

The important innovation is:

> **Family identification and eligibility discovery happen automatically.**

---

# PHASE 13 — CITIZEN DASHBOARD

Create these sections:

```text
Dashboard
├── Family ID
├── Family Verification
├── Family Members
├── Benefits
├── Applications
└── Profile
```

Dashboard cards:

```text
Family ID
Members
Eligible Benefits
Applications
Pending Applications
```

Main CTA:

```text
Find Benefits for My Family
```

---

# PHASE 14 — ADMIN / DEMO DASHBOARD

Create a very lightweight admin dashboard.

Admin can:

```text
View Families
View Applications
Manage Demo Schemes
View Basic Statistics
```

Statistics:

```text
Total Families
Total Citizens
Total Applications
Eligible Benefits
Approved Applications
```

Do not make admin necessary for normal family creation.

The purpose is only:

* scheme management
* demonstration
* basic monitoring

---

# PHASE 15 — FRONTEND DESIGN

Use a professional government-service style.

Design principles:

* Clean
* Accessible
* Responsive
* Simple
* Trustworthy
* Government portal inspired

Use:

* Blue/white visual language
* Cards
* Tables
* Status badges
* Clear progress indicators
* Simple navigation

Create reusable components:

```text
Navbar
Sidebar
Card
Button
Modal
Table
StatusBadge
LoadingState
ErrorState
EmptyState
```

Include a visible label such as:

```text
Hackathon Demo • Synthetic Government Data
```

This makes it clear that the Aadhaar and Ration Card numbers shown in the application are fictional.

---

# PHASE 16 — EXCEPTION HANDLING

Implement a lightweight exception model.

Possible exception types:

```text
IDENTITY_VERIFICATION_FAILED
HOUSEHOLD_NOT_FOUND
PERSON_NOT_FOUND_IN_HOUSEHOLD
DATA_MISMATCH
MULTIPLE_HOUSEHOLDS
```

Do not create complex human workflows.

Store exceptions so the system can show:

```text
Verification Issue
-------------------------
Reason:
Identity and household data
could not be automatically matched.

Status:
ACTION_REQUIRED
```

This gives us a path to future human verification without making officers part of the normal architecture.

---

# PHASE 17 — SECURITY

Implement:

* Password hashing
* JWT authentication
* Role authorization
* Input validation
* SQLAlchemy ORM
* **Do not store raw Aadhaar numbers in FamilyConnect as the primary identifier**
* Do not store real Aadhaar/Ration Card data
* No sensitive data in Family ID
* Citizen can only access their own family data
* Citizen can only view their own applications
* Admin-only scheme management
* Environment variables for secrets

Create:

```text
.env.example
```

with:

```text
DATABASE_URL=
JWT_SECRET_KEY=
AADHAAR_SERVICE_URL=
RATION_SERVICE_URL=
```

---

# PHASE 18 — DOCKER COMPOSE

Docker Compose should run:

```text
frontend
backend
postgres
mock-aadhaar
mock-ration
```

Example:

```text
docker compose up --build
```

Everything should start successfully.

The backend should communicate with:

```text
http://mock-aadhaar:8000
http://mock-ration:8000
```

inside Docker networking.

Do not hardcode localhost for service-to-service communication.

---

# PHASE 19 — SEED DATA

Create realistic fictional demo data.

## Mock Aadhaar

20–30 fictional citizens.

Example:

```text
PERSON-10001 → 482719365041
PERSON-10002 → 617384920156
PERSON-10003 → 835261749302
PERSON-10004 → 294817563920
```

## Mock Ration

10–15 fictional households.

Example:

```text
739258146203
581426937105
864219573048
315792684201
```

All identifiers must be synthetic.

## FamilyConnect

Some families should already be resolved.

## Schemes

8–10 demo schemes.

## Scheme Rules

Several rules for each scheme.

## Applications

Create examples in different states.

Important demo scenarios:

```text
Scenario 1:
New citizen → New Family

Scenario 2:
Second citizen → Existing Family

Scenario 3:
Citizen → Eligibility → Application

Scenario 4:
Aadhaar/Ration mismatch

Scenario 5:
No household found
```

---

# PHASE 20 — TESTING

Write tests for the most important business logic.

## Family Resolver Tests

Test:

```text
New household → creates Family ID
Existing household → links existing Family ID
Multiple members → same Family ID
Mismatch → exception
No household → exception
```

## Eligibility Tests

Test:

```text
Eligible
Not eligible
Multiple members
Multiple rules
Invalid rule
```

## API Tests

Test:

```text
Registration
Login
Family resolution
Family profile
Scheme listing
Eligibility
Application
```

---

# PHASE 21 — DOCUMENTATION

Create:

```text
docs/
├── architecture.md
├── database.md
├── api.md
├── family_resolution.md
├── eligibility_engine.md
├── mock_government_services.md
├── security.md
└── roadmap.md
```

## architecture.md

Explain:

* Overall architecture
* Main components
* Mock government integrations
* Family Resolver
* Eligibility Engine
* Data flow

## database.md

Include:

* ER diagram
* Tables
* Relationships
* Constraints

## api.md

Document important APIs.

## family_resolution.md

Explain all five cases:

```text
1. New family
2. Existing family
3. Multiple members
4. Data mismatch
5. No household
```

## mock_government_services.md

Explain:

* Why mock services exist
* Mock Aadhaar API
* Mock Ration API
* Example responses
* How real authorized providers could replace them in production
* Explicitly state that all identifiers and datasets are synthetic

## roadmap.md

Separate:

```text
MVP
V2
Future
```

---

# PHASE 22 — FUTURE V2

Do not implement these now.

Document them only.

## Identity

* Real authorized Aadhaar/e-KYC integration
* Gujarat SSO integration
* Additional government identity providers

## Household

* More government household databases
* Life-event synchronization
* Family membership changes
* Address updates

## Intelligence

* AI government scheme assistant
* RAG over official scheme documents
* Natural-language scheme search
* Explainable benefit recommendations

## Data Quality

* Advanced duplicate detection
* Entity resolution
* Data conflict resolution
* Fraud/anomaly detection

## Notifications

* SMS
* Email
* WhatsApp
* Push notifications

## Analytics

* District-level benefit coverage
* Unclaimed-benefit detection
* Scheme utilization
* Beneficiary analytics

---

# PHASE 23 — FINAL DEMO FLOW

The application must support this exact demo.

## Demo 1 — First family member

```text
Open FamilyConnect
       ↓
Register
       ↓
Enter synthetic 12-digit Aadhaar Number
       ↓
Mock Aadhaar verifies identity
       ↓
FamilyConnect calls Mock Ration API
       ↓
Household found
       ↓
No existing Family ID
       ↓
Family ID automatically created
       ↓
Show:

GJ-FAM-8X29KQ
```

Example:

```text
Aadhaar:
835261749302

Ration Card:
739258146203

Generated Family ID:
GJ-FAM-8X29KQ
```

---

## Demo 2 — Second family member

Logout.

Register another citizen belonging to the same mock ration card.

```text
Aadhaar Verification
       ↓
Ration Card Lookup
       ↓
Existing Family Found
       ↓
NO new Family ID
       ↓
Link person to existing family
```

Show:

```text
GJ-FAM-8X29KQ

Members: 4
```

This demonstrates automatic family consolidation.

---

## Demo 3 — Benefit discovery

Login as family member.

Click:

```text
Find Benefits for My Family
```

Show:

```text
Family Profile
       ↓
Eligibility Engine
       ↓
Eligible Schemes
```

Example:

```text
✓ Student Scholarship
✓ Farmer Assistance
✓ Housing Assistance
```

Click one.

Show exactly why the family qualifies.

---

## Demo 4 — Application

```text
Eligible Scheme
      ↓
Apply
      ↓
Application Submitted
      ↓
Track Status
```

---

## Demo 5 — Data mismatch

Use a deliberately configured mock record.

Mock Aadhaar:

```text
Aadhaar Number: 835261749302
Person Reference: PERSON-10003
Name: Rahul Patel
DOB: 2004-07-15
```

Mock Ration:

```text
Ration Card Number: 739258146203
Person Reference: PERSON-10003
Name: Rahul Patel
DOB: 2003-07-15
```

Show:

```text
⚠ Automatic verification failed

Reason:
Identity data and household data
do not match.
```

This demonstrates that the system does not blindly trust conflicting data.

---

# PHASE 24 — FINAL QUALITY CHECK

Before declaring the project complete, verify:

### Identity

* [ ] Mock Aadhaar works
* [ ] Synthetic Aadhaar numbers contain exactly 12 digits
* [ ] Invalid identity is rejected
* [ ] Registration works
* [ ] Login works

### Household

* [ ] Mock Ration service works
* [ ] Synthetic Ration Card numbers use realistic numeric formatting
* [ ] New family gets Family ID
* [ ] Existing family is detected
* [ ] Multiple citizens resolve to same Family ID
* [ ] Mismatch is detected
* [ ] Missing household is handled

### Family

* [ ] Family profile works
* [ ] Members display correctly
* [ ] Family ID is unique
* [ ] Family source is recorded

### Schemes

* [ ] Demo schemes exist
* [ ] Rules exist
* [ ] Eligibility engine works
* [ ] Reasons are displayed

### Applications

* [ ] Citizen can apply
* [ ] Application status works
* [ ] Application can be reviewed in demo/admin flow

### UI

* [ ] Citizen dashboard works
* [ ] Family page works
* [ ] Benefits page works
* [ ] Application page works
* [ ] Admin dashboard works
* [ ] Synthetic-data disclaimer is visible

### Infrastructure

* [ ] Docker Compose works
* [ ] Database migrations work
* [ ] Seed data works
* [ ] README is complete
* [ ] No secrets committed
* [ ] Tests pass

---

# MOST IMPORTANT IMPLEMENTATION PRINCIPLE

Do not try to build everything simultaneously.

Implement strictly in this order:

```text
PHASE 0
Project Setup
     ↓
PHASE 1
Mock Aadhaar
     ↓
PHASE 2
Mock Ration
     ↓
PHASE 3
Database
     ↓
PHASE 4
Authentication
     ↓
PHASE 5
Family Resolver ⭐
     ↓
PHASE 6
Family Profile
     ↓
PHASE 7
Resolution API
     ↓
PHASE 8
Schemes
     ↓
PHASE 9
Eligibility Engine ⭐
     ↓
PHASE 10
Benefit Discovery
     ↓
PHASE 11
Applications
     ↓
PHASE 12
Automated Application Flow
     ↓
PHASE 13
Citizen Dashboard
     ↓
PHASE 14
Admin Dashboard
     ↓
PHASE 15
UI Polish
     ↓
PHASE 16
Exceptions
     ↓
PHASE 17
Security
     ↓
PHASE 18
Docker
     ↓
PHASE 19
Seed Data
     ↓
PHASE 20
Testing
     ↓
PHASE 21
Documentation
```

After completing each phase:

1. Run the relevant tests.
2. Start the application.
3. Verify that previous functionality still works.
4. Fix errors before proceeding.
5. Do not move to the next phase with broken functionality.

---

# FINAL PRODUCT VISION

The final MVP should demonstrate this simple but powerful concept:

```text
              CITIZEN
                 │
                 ▼
        Mock Government ID
                 │
                 ▼
       Identity Verification
                 │
                 ▼
        Mock Ration Card Data
                 │
                 ▼
        ┌───────────────────┐
        │  FAMILY RESOLVER  │
        └─────────┬─────────┘
                  │
         ┌────────┴────────┐
         ▼                 ▼
    New Family        Existing Family
         │                 │
         ▼                 ▼
     Create ID          Link ID
         │                 │
         └────────┬────────┘
                  ▼
              FAMILY ID
                  │
                  ▼
          FAMILY PROFILE
                  │
                  ▼
        ELIGIBILITY ENGINE
                  │
                  ▼
        GOVERNMENT SCHEMES
                  │
                  ▼
        BENEFIT DISCOVERY
                  │
                  ▼
             APPLICATION
                  │
                  ▼
          APPLICATION STATUS
```

The central value proposition is:

> **"Verify once, create a unified Family ID automatically, and discover the government benefits your family may be eligible for."**

The system should feel like a **real government digital-service architecture**, while clearly using fictional/mock government data for the hackathon.

All Aadhaar numbers, Ration Card numbers, personal records, household records, and scheme data used in this MVP must be **synthetic data created solely for demonstration purposes**.
