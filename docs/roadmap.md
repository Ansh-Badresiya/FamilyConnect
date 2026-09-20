# Future Roadmap (V2)

The current system acts as a hackathon MVP demonstrating the core value proposition: automating family profiles and benefit discovery.

Future versions would aim to implement the following production features:

## 1. Advanced Verification (e-KYC)
- Integration with real UIDAI Aadhaar APIs (e-KYC) for OTP/Biometric based login and demographic retrieval.
- Complete migration away from mock endpoints.

## 2. Multi-department Integration
- Connecting to Land Record APIs (e.g. AnyROR), Income Tax APIs, and Vehicle Registration APIs to build a richer, more accurate 360-degree family profile.
- Utilizing these external sources for automated eligibility without requiring self-declared income data.

## 3. Asynchronous Resolution
- Migrating the synchronous `FamilyResolver` engine to an asynchronous message queue (e.g., Celery/RabbitMQ) for handling high-volume background data processing and periodic synchronization with government databases.

## 4. Complex Scheme Rules
- Implementing a robust rules engine (e.g., Drools or a sophisticated custom AST evaluator) capable of executing advanced boolean logic and cross-field comparisons for eligibility.

## 5. Security & Auditing
- Implementing comprehensive audit logs for all data mutations.
- Strict data masking and granular role-based access control (RBAC) ensuring officers only access data relevant to their specific departmental jurisdiction.
