# API Documentation

The FamilyConnect backend is built with FastAPI. Complete interactive documentation is available by running the server and visiting `/api/docs`.

## Key Endpoints

### Authentication
- `POST /api/auth/register`: Register a new citizen by validating a 12-digit mock Aadhaar number against the external Mock Aadhaar service.
- `POST /api/auth/login`: Authenticate an existing user and return a JWT access token.
- `GET /api/auth/me`: Get the profile of the currently authenticated user.

### Families
- `POST /api/families/resolve`: Trigger the Family Resolver engine to automatically fetch the user's household data from the Mock Ration service and link them to a Family ID.
- `GET /api/families/me`: Retrieve the unified family profile and all members.

### Eligibility & Applications
- `GET /api/eligibility/my-benefits`: Evaluate the authenticated user's family profile against all active scheme rules and return eligible/ineligible categories.
- `POST /api/applications`: Submit a new application for a scheme.
- `GET /api/applications/me`: Retrieve all submitted applications for tracking.

### Admin
- `GET /api/admin/stats`: Get system-wide KPIs.
- `GET /api/admin/families`: Retrieve all registered families.
- `GET /api/admin/applications`: Retrieve all submitted applications.
