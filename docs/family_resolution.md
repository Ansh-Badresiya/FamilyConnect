# Family Resolution Engine

The Family Resolution engine (`FamilyResolver`) handles linking an individual citizen to a centralized Family Profile. It eliminates the need for manual officer review by attempting to correlate verified identity references with government household datasets.

## The 5 Resolution Cases

### 1. New Family
- **Trigger**: The citizen's identity is verified, and a household (ration card) record is found. No `FamilyConnect` family exists for that ration card reference yet.
- **Action**: Generates a new `family_id`, creates a new Family record, maps all members from the household dataset as new `Person` entries, and links the citizen.

### 2. Existing Family
- **Trigger**: The citizen's identity is verified, and their ration card record already maps to an existing `family_id` in the system.
- **Action**: Links the registering citizen to the existing family. No duplicate families are created.

### 3. Multiple Members
- **Trigger**: Multiple individuals belonging to the same household register sequentially.
- **Action**: The system correlates their shared external household reference and correctly converges them all into the exact same Family ID.

### 4. Data Mismatch
- **Trigger**: Demographic data (e.g. Date of Birth, Name) fetched from the Identity provider significantly differs from the data stored in the Household provider.
- **Action**: Raises a `VERIFICATION_EXCEPTION`. The system flags this discrepancy rather than blindly linking profiles.

### 5. No Household
- **Trigger**: Identity is verified, but a query against the household provider returns no matches.
- **Action**: Raises a `NO_HOUSEHOLD_FOUND` exception. The system does not invent a family ID; it requires an exception pathway.
