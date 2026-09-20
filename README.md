# FamilyConnect Gujarat

>  **Hackathon Demo** — All citizen data is entirely synthetic. No real Aadhaar numbers or personal records are used.

A unified citizen-facing platform that automatically links government identity (Aadhaar) with household records (Ration Card) to generate verified Family Profiles and discover eligible government scheme benefits.

---

##  Quick Start

**Prerequisites:** Docker & Docker Compose

```bash
git clone <repo-url>
cd Pravi-Hackthon
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API + Swagger | http://localhost:8000/api/docs |
| Mock Aadhaar Service | http://localhost:8001 |
| Mock Ration Service | http://localhost:8002 |

---

##  Test Accounts (Mock Aadhaar Numbers)

Register with any of these synthetic Aadhaar numbers to explore the app:

| Aadhaar Number | Name | Family / Household |
|---|---|---|
| `482719365041` | Rajesh Patel (HEAD) | BPL — Surendranagar |
| `617384920156` | Meena Patel | BPL — Surendranagar |
| `835261749302` | Rahul Patel | BPL — Surendranagar |
| `751936284105` | Suresh Shah (HEAD) | APL — Ahmedabad |
| `938475610293` | Kamla Shah | APL — Ahmedabad |
| `504938172645` | Anita Mehta (HEAD) | BPL — Surat |
| `727364810529` | Nilam Joshi (HEAD) | BPL — Rajkot |
| `839472615084` | Gopal Sharma (HEAD) | BPL — Gandhinagar |
| `127564839201` | Lata Sharma | BPL — Gandhinagar |
| `728401693857` | Ajay Trivedi (HEAD) | APL — Mehsana |

> After registration, click **"Link My Household"** on the dashboard to auto-resolve your family profile from the mock Ration database.

---

##  Key Features

- **Zero-touch Family Linking** — Auto-merges Aadhaar identity with Ration Card household data.
- **Eligibility Engine** — Dynamically evaluates family against active government schemes.
- **Change Requests** — Citizens cannot directly edit verified data; all changes go through an approval workflow.
- **Add / Remove Members** — Report births (Add Member) and deaths (Remove Member) via the change request pipeline.
- **Family Transfers** — Citizens can transfer to a new household (e.g., after marriage) by verifying the target household via a spouse's Aadhaar.

---

##  Architecture

```
React Frontend (Vite)
       │  REST / JWT
       ▼
  FastAPI Backend
  ├── FamilyResolver Engine ──► Mock Aadhaar API
  │                         └─► Mock Ration API
  ├── Eligibility Engine
  ├── Change Request Manager
  └── Family Transfer Service
       │  SQLAlchemy ORM
       ▼
  PostgreSQL Database
```

See [`docs/architecture.md`](docs/architecture.md) for full Mermaid diagrams (ER, sequence, component).

---

##  Project Structure

```
Pravi-Hackthon/
├── frontend/          # React + Vite + TypeScript
├── backend/           # FastAPI + SQLAlchemy + Alembic
│   ├── app/api/       # Route handlers
│   ├── app/models/    # DB models
│   ├── app/services/  # Business logic
│   └── alembic/       # DB migrations
├── mock-aadhaar/      # Synthetic identity service
├── mock-ration/       # Synthetic household service
└── docker-compose.yml
```
