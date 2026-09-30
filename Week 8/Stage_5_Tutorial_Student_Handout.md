Assignment 2- Case Study (8995-G level Task)

Stage 5 Tutorial Activities

Architecture and Responsibility

Week 8 | 60 minutes

# Activity 1 - Where Does This Belong?

| **Responsibility**                  | **Layer**                | **Reason**                                                                  |
| ----------------------------------- | ------------------------ | --------------------------------------------------------------------------- |
| Read menu input                     | Presentation             | This is part of user interaction and I/O                                    |
| Check appointment status transition | Domain or Service        | This is business logic; status rules belong to domain/service               |
| Coordinate booking use case         | Service                  | This is the orchestration of business workflow                              |
| Execute SQL INSERT                  | Persistence / Repository | Data access is not presentation; it belongs to storage layer                |
| Format confirmation message         | Presentation             | UI formatting belongs in presentation layer                                 |
| Find appointment by ID              | Repository or Service    | Lookup logic is repository responsibility; service may coordinate retrieval |

# Activity 2 - Architecture Smell Hunt

\- A SmartCare file contains input(), SQL, appointment conflict rules, printing and validation. Identify at least five architecture problems and propose a layer for each responsibility.

_1\. Persistence logic is embedded in business workflow_

- Example: SQL statements directly inside booking logic
- Problem: business code becomes database-aware

_2\. Business rules are not centralized_

- Example: duplicate booking checks and status validation appear in multiple places
- Problem: inconsistent rule enforcement

3\. Validation is scattered

- Example: some checks are in input handling while others are in service logic
- Problem: hard to maintain and verify

_4\. Presentation formatting is tied to domain behavior_

- Example: printing formatted appointment text from inside booking logic
- Problem: changes to UI affect business code

_5\. Tight coupling to concrete data structure_

- Example: direct use of lists and dictionary records
- Problem: cannot swap implementation without rewriting code

_6\. Hidden global state_

- Example: shared appointment list or global variables used across functions
- Problem: test interference and unpredictable behavior

_7\. Hard to extend or modify_

- Example: adding a new appointment status or new validation requires changing multiple functions
- Problem: risk of regressions

_8\. No abstraction for persistence_

- Example: no repository interface
- Problem: code cannot be easily tested with fake data

# Activity 3 - SOLID Without Overengineering

\- ClinicManager handles every use case. Which principle is threatened?

**🡺 Single Responsibility Principle (SRP):**

- If 1 class handles patient management, scheduling, reporting, billing, and validation, it becomes broad
- It cannot be changed for one use case without affecting unrelated behavior
- It becomes difficult to test and reason about

\- AppointmentService imports sqlite3 directly. What dependency concern exists?

**🡺 This violates Dependency Inversion Principle (DIP):**

- Business service should not directly depend on a concrete database library
- The service should depend on an interface/abstraction such as AppointmentRepository
- A concrete DB dependency makes the service harder to test and harder to change

\- A repository interface has 20 methods but a client needs two. What concern exists?

&nbsp;**🡺 Interface Segregation Principle (ISP):**

- A wide interface forces consumers to depend on methods they do not use
- Better to create smaller interfaces such as:
  - AppointmentRepositoryRead
  - AppointmentRepositoryWrite
  - or one minimal repository contract for the needs of that feature

\- Should every class have an interface? Explain.

**🡺 No, not every class needs an interface.**

_+) Use interfaces when:_

- There are multiple implementations
- Dependencies are swapped or mocked
- To decouple service from concrete implementation
- Unit tests need fake implementations

_+) Do not create interfaces when:_

- The class is a simple value object
- There is only one implementation
- The abstraction would be artificial and adds no value

**🡺 So, the rule is not "every class needs an interface," but "every dependency that may vary should be abstracted."**

# Activity 4 - AI Architecture Critique

\- AI proposes microservices, an event bus, six interfaces and a dependency-injection framework. Decide what to reject, defer or keep using current requirements.

| **Architectural Proposal**         | **Decision**          | **Rationale & Notes**                                                                                                                                                                                  |
| ---------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Microservices**                  | **Reject**            | The current project is small and single-clinic. There are no requirements justifying distributed systems or separate deployments. Introduces too much operational complexity for v0.2/v0.5.            |
| **Event Bus**                      | **Reject**            | Event-driven architecture is only useful for asynchronous workflows or multiple independent systems. It adds complexity without clear benefits for current requirements.                               |
| **6 Interfaces (per class)**       | **Reject**            | Too much abstraction for the current solution size. Violates YAGNI (You Aren't Gonna Need It). Interfaces should only be used where dependencies actually vary.                                        |
| **Dependency Injection Framework** | **Keep** _(Modified)_ | Keep simple constructor injection where needed (e.g., injecting repository implementations into AppointmentService) to improve testability. Reject heavyweight DI frameworks unless the project grows. |
| **Advanced Architecture Choices**  | **Defer**             | Revisit microservices, event buses, and elaborate DI patterns only if future requirements demand notification processing, external integrations, horizontal scaling, or background tasks.              |

🡺 Ultimately, the system will utilize a lightweight layered architecture, which is divided into Presentation, Service, Domain, Repository, and Persistence tiers to successfully achieve maintainability, testability, and separation of concerns without succumbing to overengineering.