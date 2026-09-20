# Database Schema

FamilyConnect utilizes a PostgreSQL database using SQLAlchemy as an ORM.

## ER Relationships

- **User**: Connects login credentials to a `Person` profile.
- **Person**: Core citizen profile containing individual demographic data.
- **Family**: The unified household entity (the 'Family ID').
- **FamilyMembership**: A many-to-many join connecting `Person` profiles to a `Family`. Contains relationship metadata (e.g., HEAD, SON).
- **IdentityRecord**: Logs verification sources (e.g., Mock Aadhaar).
- **FamilySource**: Logs household data provenance (e.g., Mock Ration Card).
- **Scheme**: A master catalogue of active government schemes.
- **SchemeRule**: JSON-driven rules associated with a `Scheme`.
- **Application**: Tracks a Family's application to a specific Scheme.

## Key Constraints
1. A citizen may only have one `ACTIVE` family membership at a time.
2. `family_id` strings (e.g. GJ-FAM-8X29KQ) are strictly unique.
3. Passwords must be hashed using bcrypt/passlib.
4. Raw government identity numbers (like Aadhaar) are explicitly NOT stored as primary keys; we utilize internal reference strings instead.
