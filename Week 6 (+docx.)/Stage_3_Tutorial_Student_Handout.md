Assignment 2-Case Study

Stage 3 Tutorial Activities

From Requirements to Domain Models

Week 6 | 60 minutes

# Candidate Concepts

| **Candidate**  | **Class?**  | **Reason**                                                                                                                                                                |
| -------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _Patient_      | ✓ YES       | Core domain entity. Represents clinic patient with identity, demographics, contact info. Essential for appointment linkage and search.                                    |
| _Practitioner_ | ✓ YES       | Core domain entity. Represents clinic staff with schedule and availability. Central to appointment assignment and conflict detection.                                     |
| _Appointment_  | ✓ YES       | Core domain entity. Represents booking linking patient + practitioner + time. Implements all booking logic.                                                               |
| _Name_         | ✗ NO        | Attribute, not entity. Patient.name and Practitioner.name are string attributes. No logic justifies separate class.                                                       |
| _Clinic_       | ✗ NO (v0.2) | Out of scope. v0.2 assumes single clinic. Multi-location support deferred to v0.3+. No FR or NFR mentions clinic as manageable entity.                                    |
| _Database_     | ✗ NO        | Infrastructure/persistence layer, not domain. Domain model is persistence-agnostic.                                                                                       |
| _Cancellation_ | ✗ NO        | Attribute, not class. FR-07 specifies dropdown list of reasons stored as string attribute on Appointment. No logic justifies separate class.                              |
| _Status_       | ✗ NO        | Enum attribute, not class. Status transitions (Pending → Confirmed →Completed/Cancelled) implemented as Enum on Appointment. Creating separate class over-engineers v0.2. |

# CRC Cards

## Patient

| **Responsibilities**                                                                                          | **Collaborators**                                                 |
| ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Store patient identity data - patient_id, name, DOB, phone, email, medical_notes                              | 🡺 Appointment - Patient has many appointments over time           |
| Generate/assign unique patient ID automatically on registration                                               | 🡺 User - Receptionist (user) creates patient records              |
| Validate patient data - Ensure non-empty name, valid email format, valid DOB (not future)                     | 🡺 SecurityManager - Encrypt phone, email, DOB before storage      |
| Enable patient lookup - Search by full name or patient ID with 2-second response (FR-02, NFR-04)              | 🡺 AppointmentHistory - Track patient's appointment change history |
| Maintain patient profile immutability - Once created, patient demographics don't change (or change is logged) | _NONE_                                                            |

## Practitioner

| **Responsibilities**                                                                                           | **Collaborators**                                                                         |
| -------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Store practitioner identity - practitioner_id, name, specialty                                                 | Appointment - Practitioner has many appointments (can see multiple patients/day)          |
| Manage working hours - Define standard clinic hours (8 AM-6 PM Mon-Fri) per practitioner                       | AppointmentReport - Report generates utilization % (booked slots / available slots)       |
| Define blocked time - Add lunch breaks, admin time, days off to block practitioner from bookings               | User - Practitioner (user) views own schedule (FR-12)                                     |
| Display available time slots - Return free slots for 4-week window for booking interface (FR-06)               | SecurityManager - Audit log practitioner actions (schedule changes, availability updates) |
| Check availability - Query whether practitioner is free at specific time (used by Appointment.check_overlap()) | _NONE_                                                                                    |

## Appointment

| **Responsibilities**                                                                                        | **Collaborators**                                                                                 |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Store appointment data - appointment_id, patient_id, practitioner_id, time, status, duration (30 min fixed) | Patient - Each appointment belongs to exactly patient                                             |
| Implement business rule BR-1 - Prevent overlapping time slots for same practitioner on same day (FR-04)     | Practitioner - Each appointment is with exactly 1 practitioner                                    |
| Call check_overlap() at booking time - Query Practitioner.check_availability() before creating appointment  | AppointmentHistory - Log every change (creation, status, cancellation, reschedule) with timestamp |
| Manage appointment lifecycle - Transition status: Pending→Confirmed→Completed or Cancelled (FR-05, BR-2)    | User - Receptionist/Practitioner perform actions; audit logged                                    |
| Record cancellation details - Store cancellation_reason and cancellation_timestamp (FR-07)                  | SecurityManager - Audit log all appointment actions                                               |

# Relationship Reasoning

\- Patient to Appointment: which relationship and why?

- Relationship & Multiplicity: Directed Association (1 Patient to 0..\* Appointments), formatted as Patient 1 ────── \* Appointment.
- Domain Justification: Models recurring clinical care (such as follow-ups and annual check-ups). A patient profile can exist with zero scheduled visits (minimum: 0) and accrue an unlimited number of interactions over time (maximum: unlimited).
- Requirement Evidence: Directly tied to FR-09 (tracking historical appointments) and FR-10 (generating per-patient analytics).
- Technical Implementation: Executed by placing patient_id as a foreign key in the Appointment model, referencing Patient.patient_id.

\- Practitioner to Appointment: what multiplicity?

- **Relationship & Multiplicity:** Directed Association (1 Practitioner to 0..\* Appointments), formatted as Practitioner 1 ────── \* Appointment.
- **Domain Justification:** Reflects standard operational workflows where providers manage full, recurring schedules. A practitioner profile can exist with zero assigned bookings (minimum: 0) and handle an unlimited volume of patient visits over time (maximum: unlimited).
- **Requirement Evidence:** Directly supported by FR-04 (double-booking prevention logic) and FR-06 (displaying daily practitioner availability).
- **Technical Implementation:** Executed by embedding practitioner_id as a foreign key within the Appointment model, referencing Practitioner.practitioner_id.

\- Should Appointment inherit from Patient?

🡺 No.

- Avoidance of Attribute Pollution: Prevents the Appointment from unnecessarily inheriting irrelevant fields.
- Appropriate Domain Modeling: Correctly structures Appointment as a transactional event via a "HAS-A" (association) relationship that links a Patient, Practitioner, and time slot.

\- Does Clinic need to own every object?

🡺 No - Out of scope for v0.2

- Single clinic assumption: v0.2 is for one small clinic (case study explicitly states "small clinic")
- Multi-location deferred: Support for multiple clinics/locations is v0.3+ feature
- Implicit scope: Objects implicitly belong to "the clinic" (system boundary)
- Simpler design: Adding Clinic as parent class adds unnecessary hierarchy for v0.2
- Implicit scope: Objects implicitly belong to "the clinic" (system boundary)

# AI Model Critique

\- Critique AI proposals: PatientManager, PractitionerManager, AppointmentManager, ClinicController, NotificationManager, ScheduleEngine.

| **AI suggestion**     | **Decision** | **Evidence**                                                                                                                                     | **Reason**            | **Model change** |
| --------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------- | ---------------- |
| _PatientManager_      | REJECT       | Considered an architectural anti-pattern since the Patient class directly encapsulates its own operations, making an external manager redundant. | Anti-pattern          | X                |
| _PractitionerManager_ | REJECT       | Adds unnecessary indirection because Practitioner already cohesively handles both its profile data and availability logic.                       | Anti-pattern          | X                |
| _AppointmentManager_  | MODIFY       | Current v0.2 booking workflows are simple. AI noted that complex multi-step processes or notifications should be introduced.                     | Workflow orchestrator | v0.2             |
| _ClinicController_    | REJECT       | Violates architectural layering principles by introducing application controller logic into the core domain model.                               | Layer violation       | X                |
| _NotificationManager_ | REJECT       | Out of scope for release v0.2; explicitly postponed to version 0.3+ during Stage 2 planning.                                                     | Out of scope          | v0.3             |
| _ScheduleEngine_      | ACCEPT       | Fixed 30-minute time slots keep v0.2 scheduling straightforward                                                                                  | Abstraction           | v0.2             |

🡺 Rejected Suggestions: Four abstractions (PatientManager, PractitionerManager, ClinicController, and NotificationManager) were rejected due to architectural anti-patterns, layering violations, or being out of scope for the v0.2 release.

🡺Accepted & Modified Changes: ScheduleEngine was accepted for v0.2 to handle fixed 30-minute slot abstractions, while AppointmentManager was modified to orchestrate simple booking workflows.

🡺 Core Architectural Rationale: Decisions prioritized direct domain class encapsulation (keeping logic inside Patient and Practitioner) and avoiding premature complexity prior to future versions like v0.3.