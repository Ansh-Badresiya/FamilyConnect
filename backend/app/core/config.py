import os

class Settings:
    PROJECT_NAME: str = "FamilyConnect Gujarat MVP"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://familyconnect:familypassword@db:5432/familyconnect_db"
    )
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecretkey12345")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    AADHAAR_SERVICE_URL: str = os.getenv("AADHAAR_SERVICE_URL", "http://mock-aadhaar:8000")
    RATION_SERVICE_URL: str = os.getenv("RATION_SERVICE_URL", "http://mock-ration:8000")

settings = Settings()
