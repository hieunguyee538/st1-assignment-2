SmartCare v0.5 - Architecture and Refactoring Workbook

Week 8 student resource

# Current Architecture Problems

| **Problem**                              | **Evidence**                                                                  | **Impact**                                     | **Refactoring**                                                           |
| ---------------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------- |
| Business logic mixed with presentation   | User interface prints appointment details and also validates appointment data | Hard to test; UI and logic are tightly coupled | Move I/O to Presentation layer; keep service/domain logic separate        |
| Duplicate logic across classes           | Validation logic repeated in multiple places                                  | Inconsistency and maintenance cost             | Centralize validation in domain/service layer                             |
| Direct data manipulation in app flow     | App code reads and writes lists/dictionaries directly                         | Hard to swap storage mechanism                 | Introduce repository abstraction                                          |
| Overbooking logic not centralized        | duplicate checks are handled ad hoc                                           | Scheduling bugs and inconsistent booking rules | Move conflict detection to AppointmentService or Appointment domain logic |
| No clear persistence boundary            | Data storage is embedded in app logic                                         | Hard to change from memory to DB               | Add repository interface and persistence adapters                         |
| Tight coupling to concrete storage       | Code depends on a specific data structure or file format                      | Difficult to scale or test                     | Depend on repository interface, not concrete storage                      |
| Mixed responsibilities in domain objects | Domain models know too much about UI, formatting, and storage                 | Violates single responsibility                 | Keep domain models focused on data and business rules only                |

# Layer Responsibilities

| **Layer**    | **Responsibilities**                                                                            | **Must not contain**                                       |
| ------------ | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Presentation | User interface, input capture, output display, validation messages, navigation                  | Business rules, database logic, persistence API calls      |
| Service      | Coordination of use cases such as booking, cancellation, rescheduling, validation orchestration | UI code, SQL, direct storage implementation                |
| Domain       | Business objects, invariants, status logic, appointment rules                                   | Console printing, database access, framework-specific code |
| Repository   | Abstract persistence access, read/write operations, domain object retrieval                     | UI logic, scheduling rules, display logic                  |
| Persistence  | Concrete DB or file storage implementation, repository adapters                                 | Domain rules, presentation flow, business workflows        |

# Architecture Diagram

\- Insert SmartCare v0.5 architecture and dependency direction.

\- SmartCare v0.5 layered architecture:

_\--> Presentation ↓ depends on Service ↓ depends on Domain ↓ depends on Repository abstraction ↓ implemented by Persistence layer_

\- High-level dependency direction:

- UI depends on app service
- Service depends on domain models
- Domain depends on repository interfaces
- Repository implementations depend on database/persistence technology

\- Example simplified diagram: Presentation Layer └── AppointmentController / CLI ↓ AppointmentService ↓ Patient / Practitioner / Appointment ↓ AppointmentRepository (interface) ↓ SQLiteAppointmentRepository / InMemoryAppointmentRepository **🡺 A .py file.**

\[ PRESENTATION LAYER \] - Handles user inputs, routing, and console outputs

├── main.py (Application entry point / DI container)

├── cli/

│ ├── appointment_cli.py (Parses user commands for scheduling)

│ └── patient_cli.py (Parses user commands for patient management)

└── views/

└── console_view.py (Formats data for terminal display)

│

│ (Depends on & delegates commands to)

↓

\[ APPLICATION SERVICE LAYER \] - Orchestrates workflows and cross-entity transactions

├── appointment_service.py (Coordinates booking, overlap checks, and saving)

├── patient_service.py (Coordinates patient registration workflows)

└── practitioner_service.py(Coordinates practitioner availability workflows)

│

│ (Depends on, instantiates, and mutates)

↓

\[ DOMAIN LAYER \] - Pure business logic, state transitions, and core entities

├── models/

│ ├── appointment.py (Core aggregate; handles state & lifecycle rules)

│ ├── appointment_status.py (Enum enforcing fixed transition states)

│ ├── patient.py (Patient entity and specific rules)

│ └── practitioner.py (Practitioner entity and schedule bounds)

└── rules/

└── validation.py (Domain-level invariant checks)

│

│ (Domain defines the contract for data needs)

↓

\[ REPOSITORY ABSTRACTION \] - Interface contracts for data access (Inversion of Control)

├── repository_interfaces.py

├── appointment_repository.py (ABC: save, find_by_id, find_by_practitioner_and_date)

├── patient_repository.py (ABC: save, find_by_id)

└── practitioner_repository.py(ABC: save, find_by_id)

▲

│ (Persistence realizes/implements the contract)

│

\[ PERSISTENCE LAYER \] - Concrete database interactions and infrastructure

├── database.py (DB connection and transaction management)

├── sqlite_appointment_repository.py (Executes SQL queries against SQLite)

├── sqlite_patient_repository.py (Executes SQL queries against SQLite)

└── InMemoryAppointmentRepository (In-memory arrays used for unit testing)

**SMARTCARE v0.5 DETAILED ARCHITECTURE**

**\====================================================================================**

# SOLID Review

| **Principle** | **Relevant?** | **Evidence**                                                                                           | **Decision** |
| ------------- | ------------- | ------------------------------------------------------------------------------------------------------ | ------------ |
| SRP           | ✓Yes✓         | AppointmentService handles workflow; Appointment handles appointment state; repository handles storage | Accept       |
| OCP           | ✓Yes✓         | Repositories can be changed without modifying business logic                                           | Accept       |
| LCP           | ✓Yes✓         | Concrete repositories can be swapped without breaking service contracts                                | Accept       |
| LSP           | ✓Yes✓         | Any repository implementation should satisfy same contract for appointment queries/saves               | Accept       |
| ISP           | ✓Yes✓         | Repository interfaces should define only relevant methods rather than broad all-in-one interface       | Accept       |

# AI Architecture Review

| **AI suggestion**                          | **Observed problem?**                              | **Decision** | **Reason**                                                                | **Verification**                                              |
| ------------------------------------------ | -------------------------------------------------- | ------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------- |
| _Add AppointmentService_                   | Business workflow mixed with UI and data access    | Accept       | Service layer is needed to coordinate appointment logic                   | Confirm booking/cancellation workflow moved out of UI         |
| _Introduce repository abstraction_         | Direct storage logic is tied to business logic     | Accept       | Needed for testability and persistence independence                       | Replace SQLite with in-memory repository in tests             |
| _Separate domain models from presentation_ | UI logic currently embedded in domain-like code    | Accept       | Prevents UI concerns from polluting domain rules                          | Verify models contain no print() calls                        |
| _Add NotificationService_                  | Current app has no notification capability in v0.2 | Reject       | Out of scope; not required by SmartCare requirements                      | No evidence in requirements; defer to future version          |
| _Add ClinicController_                     | Could become application orchestrator              | Reject       | Domain model should be simple; controllers are not core business entities | No requirement justifies controller as domain concern         |
| _Add ScheduleEngine_                       | Complex scheduling logic may emerge later          | Defer        | Keep simple for v0.5 unless requirements require more advanced scheduling | Reassess if appointment durations or policies become variable |