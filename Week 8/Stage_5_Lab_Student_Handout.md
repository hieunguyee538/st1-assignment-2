Assignment 2- Case Study (8995-G level Task)

Stage 5 Lab Activities

Refactoring SmartCare into a Layered Architecture

HUMAN ANALYSIS -> REFACTOR -> AI REVIEW -> VERIFY | 1 hour

# A - Inspect SmartCare v0.4

\- Identify domain, workflow, data-access and presentation responsibilities currently mixed together.

\- SmartCare v0.4 currently mixes responsibilities across layers. The code handles:

- Domain logic and validation in the same place as presentation/output
- User interaction and business workflow together
- Data access and persistence logic embedded inside business objects
- Appointment rules and scheduling logic not clearly separated from plain data storage

**🡺 This makes the system difficult to maintain, hard to test, and harder to extend without breaking existing behavior.**

\- Problems in v0.4:

- Appointment booking rules are mixed with printing and user I/O
- Data structures are used directly without a clear repository abstraction
- Validation and data storage are not separated from business workflow
- It is difficult to swap persistence implementation without rewriting application logic
- The application cannot easily support testing with fake data or alternate database backends

# B - Propose Architecture

\- Draw Presentation -> Service -> Domain, with Service using a Repository abstraction and Persistence implementing it.

\- Layered architecture:

- Presentation layer
  - Handles UI input/output
  - Collects user actions and displays results
  - Does not contain business rules
- Service layer
  - Contains appointment workflows such as:
    - booking
    - cancellation
    - rescheduling
    - checking slot availability
  - Coordinates domain objects and repository
- Domain layer
  - Contains core business objects:
    - Patient
    - Practitioner
    - Appointment
    - AppointmentStatus
  - Contains validation and business rules
- Repository layer
  - Abstracts storage operations
  - Defines methods such as save, find_by_id, find_all, update, delete
- Persistence layer
  - Concrete implementation of repository contracts
  - Example: SQLiteRepository or database adapter; handles actual data storage

# C - Create Package Structure

\- Create domain/, services/, repositories/, persistence/ and presentation/ or a justified equivalent. **🡺 A .py file**

# D - Introduce AppointmentService

\- Move workflow coordination into a focused service without stealing Appointment domain behaviour.

\- AppointmentService should coordinate appointment booking rules while keeping the domain model focused on data and rules. **🡺 A .py file**

_+) Responsibilities:_

1. Book an appointment
2. Validate input data
3. Check if the practitioner is free
4. Ensure appointment does not overlap with another appointment for the same practitioner
5. Save appointment to repository
6. Return a confirmation result to caller

_+) Example responsibilities of AppointmentService:_

1. create_appointment(patient_id, practitioner_id, appointment_datetime)
2. cancel_appointment(appointment_id, reason)
3. reschedule_appointment(appointment_id, new_datetime)
4. get_appointments_for_practitioner(practitioner_id, date)
5. get_appointments_for_patient(patient_id)

**🡺 Design decision: AppointmentService should not print directly to console. It should return data or domain objects to the presentation layer as this keeps business workflow logic separate from UI printing.**

# E - Repository Abstraction

\- Define a small AppointmentRepository contract using only current use-case needs.

\- Repository abstraction defines how the application interacts with stored data, without coupling domain code to a concrete database. **🡺 A .py file**

\- Benefits: +) Easier to unit test service logic using fake repositories

+) Domain logic does not depend on SQL or database implementation details

+) Can swap SQLite, in-memory storage, or a future cloud backend

\- Example repository implementations:

- InMemoryAppointmentRepository
- SQLiteAppointmentRepository

_🡺 The domain should depend on the abstraction, not the implementation._

# F - AI Architecture Review

\- Ask AI to review dependency direction, misplaced responsibilities and unnecessary complexity; request simplest justified improvements.

\--> AI review result:

- Accept: separate domain model from UI ✓✓✓
- Accept: introduce AppointmentService for workflow logic ✓✓✓
- Accept: use repository abstraction for persistence ✓✓✓
- Modify: avoid over-engineering with a heavy framework unless required
- Reject: adding notification microservice or separate Clinic service. XXX
- Keep unverified: event-driven architecture until project growth justifies it

\--> The point is not to build a complex enterprise architecture, but a layered design that is clear, testable, and maintainable.

# G - Refactor and Verify

\- Apply only justified changes and confirm required behaviour remains unchanged.

| **Refactoring Action**                                        | **Mapped Verification Checklist**                                               |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| _Move printing logic to Presentation layer_                   | Business logic remains unchanged after refactor                                 |
| _Move scheduling workflow to AppointmentService_              | Appointments can be created, cancelled, and rescheduled through service methods |
| _Move validation into domain objects and service methods_     | Appointment booking still checks practitioner availability                      |
| _Standardize repository interfaces_                           | Repository implementation can be swapped without changing service logic         |
| _Replace direct data structures with repository interactions_ | Patients can be searched without direct database logic in domain code           |
| _Keep domain models lightweight and focused_                  | Business logic remains unchanged after refactor                                 |

# H - Reflection

\- Document one AI suggestion accepted, one modified and one rejected/deferred.

+) **Accepted AI Suggestion: Implementation of AppointmentStatus as an Enum:** The AI suggested using a strict Python Enum for tracking appointment states (e.g., Scheduled, Completed, Cancelled). This was accepted entirely because it perfectly aligned with the UML specifications, preventing invalid state strings and enforcing strict domain rules without adding unnecessary complexity.

+) **Modified AI Suggestion: Repository Interface CRUD Methods:** The AI generated a standard repository interface containing save(), update(), find_all(), and delete() methods. This was modified to include only save(), find_by_id(), and find_by_practitioner_and_date(). delete() was removed because business rules dictate that canceled appointments must be retained for auditing, and find_all() was removed to prevent unbounded database queries.

+) **Rejected AI Suggestion: Domain Model Inheritance and Active Record:** The AI suggested making the Appointment class inherit from a PatientRecord base class and adding database execution logic directly into the model (Active Record pattern). This was rejected to maintain strict Separation of Concerns. An appointment _has a_ relationship with a patient; it is not a subtype. Furthermore, embedding database logic inside the domain model violates the architecture's requirement to isolate persistence in the Repository layer.

# Suggested AI prompt

Act as a software architecture reviewer. Review this small SmartCare Python system against separation of concerns, cohesion, coupling and introductory SOLID principles. Identify concrete layer violations and dependency risks. Prefer the simplest refactoring that solves an observed problem. Do not introduce frameworks, microservices or patterns unless current requirements justify them.

**System Architecture & Separation of Concerns**

- The architecture successfully separates responsibilities by ensuring that the Appointment class exclusively governs domain rules, while database access is isolated in a dedicated repository and user interaction remains in the UI or application layer.
- A concrete layer violation occurs if the domain model executes SQL directly (e.g., inside a cancel() method), as persistence is an infrastructure concern that belongs strictly in the repository layer.
- Allowing the UI to dictate whether a status transition is legal is a separation of concerns violation; the UI should only display buttons and collect inputs, leaving the domain object to enforce business rules.
- Introducing application controller logic into the core domain model, such as a proposed ClinicController, violates architectural layering principles and must be rejected.

**Cohesion & Single Responsibility Principle (SRP)**

- Code can use standard object-oriented syntax but still suffer from poor design and violate SRP if it mixes concerns by exposing status attributes to unrestricted mutation, managing notifications, or controlling presentation logic.
- The system maintains high cohesion when classes protect their own invariants; for instance, the Patient class validates its own name and the Appointment class enforces its own status transitions and cancellation rules.
- External abstraction classes like PatientManager and PractitionerManager are considered architectural anti-patterns because the core domain entities already cohesively handle their own profile data and operations.

**Coupling & Dependency Risks**

- Implementing inheritance incorrectly—such as making Appointment inherit from PatientRecord or a Patient class—creates tight coupling, unnecessary attribute pollution, and skewed domain hierarchies.
- The system accurately mitigates this risk by utilizing composition and association, linking the Appointment to external entities solely via patient_id and practitioner_id foreign keys.
- Integrating a NotificationManager introduces an unnecessary, out-of-scope dependency into the core domain that tangles business logic with messaging infrastructure.

**Recommended Simplest Refactorings**

- Extract any embedded SQL or database logic from domain methods and relocate it to a dedicated repository interface.
- Eliminate broad public status mutation by encapsulating state changes within strict lifecycle operations like confirm(), complete(), and cancel().
- Remove speculative frameworks and services (e.g., NotificationManager, AppointmentManager, PatientManager) to ensure the domain model remains lightweight, highly cohesive, and tightly aligned with the approved v0.2 UML scope.