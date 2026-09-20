from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, families, schemes, eligibility, applications, dashboard, change_requests, family_transfers

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(families.router, prefix="/api/families", tags=["families"])
app.include_router(schemes.router, prefix="/api/schemes", tags=["schemes"])
app.include_router(eligibility.router, prefix="/api/eligibility", tags=["eligibility"])
app.include_router(applications.router, prefix="/api/applications", tags=["applications"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(change_requests.router, prefix="/api/change-requests", tags=["change_requests"])
app.include_router(family_transfers.router, prefix="/api/family-transfers", tags=["family_transfers"])

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
