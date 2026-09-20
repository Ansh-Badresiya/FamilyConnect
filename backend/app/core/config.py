from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FamilyConnect Gujarat MVP"
    DATABASE_URL: str = "postgresql://familyconnect:familypassword@localhost:5432/familyconnect_db"
    JWT_SECRET_KEY: str = "supersecretkey12345"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    AADHAAR_SERVICE_URL: str = "http://mock-aadhaar:8000"
    RATION_SERVICE_URL: str = "http://mock-ration:8000"

    class Config:
        env_file = ".env"

settings = Settings()
