import os
import sys
import httpx

# Add app to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.person import Person
from app.core.config import settings

def main():
    db = SessionLocal()
    persons = db.query(Person).filter(Person.gender.in_(['U', 'Unknown'])).all()
    
    updated = 0
    for person in persons:
        try:
            resp = httpx.get(
                f"{settings.AADHAAR_SERVICE_URL}/api/v1/identity/by-reference/{person.person_reference}",
                timeout=5.0
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("found"):
                    person.gender = data.get("gender")
                    updated += 1
        except Exception as e:
            print(f"Error fetching for {person.person_reference}: {e}")
            
    db.commit()
    print(f"✅ Successfully updated {updated} records that had 'U' gender.")

if __name__ == "__main__":
    main()
