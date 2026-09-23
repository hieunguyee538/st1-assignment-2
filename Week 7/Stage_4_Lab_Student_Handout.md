Assignment 2-Case Study

Stage 4 Lab Activities

Implementing the SmartCare Domain Layer

DESIGN FIRST -> AI PAIR PROGRAMMING -> REVIEW -> VERIFY | 1hour

# A - Revisit Approved UML

\- Confirm responsibilities, attributes and relationships before coding.

**\- Appointment** is a domain entity 🡺 It handles the booking lifecycle logic.

_+) It includes the following:_

- Appointment_id, patient_id, practitioner_id, time, status, cancelation reason, and cancelation timestamp.
- Appointment Status is an enum, not a separate class.
- There are no database, notification, or service layers included.
- Overlap detection is enforced by Appointment.check_overlap().
- Status transitions must be safeguarded by validation procedures.

**\- Patient:**

_+) Attributes:_ patient_id_,_name d.o.b, phone, email, medical_notes

_+) Responsibilities:_

- Store patient information.
- Validate patient data.
- Reject invalid names, contact details, and future dates of birth.
- Provide a basic registration operation.

\- **Practitioner:**

_+) Attributes:_ practitioner_id, name, specialty

_+) Responsibilities:_

- Store practitioner information.
- Validate the practitioner ID, name, and specialty.
- Provide practitioner information for appointment assignment.

🡺 Availability management is not implemented in this stage because the task only requires the identifier, name, and specialty.

# B - Implement Patient: AI OFF

\- Implement Patient with type hints and basic validation.

🡺 A py. file

# C - Implement Practitioner: AI OFF

\- Implement Practitioner with identifier, name and specialty; no database logic.

🡺 A py. file

# D - Implement Appointment: AI ON

\- Give AI the approved Appointment UML, business rules and explicit constraints. Ask it to implement only Appointment and agreed enum/exception.

🡺 A py. file

# E - Review Generated Code

\- Check model consistency, unsupported features, public state mutation, unnecessary inheritance, invented dependencies and error handling.

**\- The model complies with the accepted UML:**

+) It employs type hints and enum and does not include database or service classes.

+) It protects status transitions directly with the addition of storing canceled appointments as objects needed.

+) It **does not** overengineer with additional classes.

+) It prevents unauthorized transitions, like:

1. Canceling an already canceled appointment.
2. Confirming a canceled or completed appointment.
3. Complete a pending appointment without confirmation.
4. Rescheduling a canceled or finished appointment.

_🡺 The review verifies that the implementation strictly adheres to the approved UML design and domain-driven principles by properly encapsulating state and business logic while avoiding unnecessary layers or coupling._

| **Assessment Area**    | **Status** | **Key Implementation Highlights**                                                                                          |
| ---------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------- |
| UML & Architecture     | Pass ✅    | Implements standard core entities (Appointment, AppointmentStatus) without database, UI, or manager clutter                |
| Encapsulation & Safety | Pass ✅    | Shields status attributes from direct mutation, avoids improper inheritance, and raises clear exceptions on invalid inputs |
| Scheduling Logic       | Pass ✅    | Flags overlapping practitioner bookings while permitting back-to-back appointments                                         |

# F - Manual Behaviour Checks

\- Create valid objects, test invalid input, cancel a scheduled appointment and attempt an illegal repeated transition.

| **Test ID** | **Behaviour checked**                        | **Test data / setup**                                                       | **Action performed**             | **Expected result**                                   | **Actual result**                            | **Status** |
| ----------- | -------------------------------------------- | --------------------------------------------------------------------------- | -------------------------------- | ----------------------------------------------------- | -------------------------------------------- | ---------- |
| _MB-01_     | Create a valid Patient                       | patient_id="P001", name "Alice Smith", valid DOB, phone, and email          | Create a Patient object          | Object is created successfully without an exception   | Patient object was created successfully      | Pass ✅    |
| _MB-02_     | Create a valid Practitioner                  | practitioner_id="DR001", name "Dr. John Doe", specialty "General Practice"  | Create a Practitioner object     | Object is created successfully without an exception   | Practitioner object was created successfully | Pass ✅    |
| _MB-03_     | Create a valid Appointment                   | appointment_id="A001", patient "P001", practitioner "DR001", valid datetime | Create an Appointment object     | Appointment is created with status PENDING            | Appointment was created with status PENDING  | Pass ✅    |
| _MB-04_     | Validate a valid Patient record              | Valid patient information                                                   | Call patient.validate()          | Validation completes without an error                 | Validation completed successfully            | Pass ✅    |
| _MB-05_     | Reject an empty patient name                 | Patient name is ""                                                          | Attempt to create a Patient      | ValueError: Patient name cannot be empty              | The expected ValueError was raised           | Pass ✅    |
| _MB-06_     | Reject a future date of birth                | DOB is later than today                                                     | Attempt to create a Patient      | ValueError: Date of birth cannot be in the future     | The expected ValueError was raised           | Pass ✅    |
| _MB-07_     | Reject an empty practitioner specialty       | Specialty is ""                                                             | Attempt to create a Practitioner | ValueError: Practitioner specialty cannot be empty    | The expected ValueError was raised           | Pass ✅    |
| _MB-08_     | Reject an empty patient ID in an appointment | patient_id=""                                                               | Attempt to create an Appointment | ValueError: Patient ID cannot be empty                | The expected ValueError was raised           | Pass ✅    |
| _MB-09_     | Reject an invalid appointment time           | Appointment time is a string instead of datetime                            | Attempt to create an Appointment | TypeError: Appointment time must be a datetime object | The expected TypeError was raised            | Pass ✅    |
| _MB-10_     | Confirm a pending appointment                | Appointment status is initially PENDING                                     | Call appointment.confirm()       | Status changes from PENDING to CONFIRMED              | Status changed to CONFIRMED                  | Pass ✅    |

# G - Refactor

\- Remove unnecessary code and make implementation simpler and design-consistent.

\- The Appointment implementation was refactored to focus solely on appointment-related domain behavior. Unneeded dependencies, unsupported features, and unrelated responsibilities were eliminated. The final class now safeguards the appointment state, enforces valid status transitions, prohibits overlapping bookings, and captures cancelation information in accordance with the approved UML.

\- If I were to refactor further, I would just make the following adjustments:

1. Consider moving overlap validation to a repository/service layer.
2. Introduce a dataclass for cleaner structure.
3. Create helper methods for faulty transitions as the project grows.
4. Keep the fixed duration simple and keep cancellation information.
5. **Removed unnecessary service classes** 🡺 No AppointmentManager, ClinicController,… was added.

🡺 The refactored Appointment class is smaller, more focused, and aligns with the authorized UML. It respects its own invariants and includes the necessary appointment business rules. It respects its own invariants and includes the necessary appointment business rules without introducing unnecessary functions.

# H - AI Engineering Log

\- Record prompt, generated contribution, decisions and verification evidence.

| **Prompt / task**                                                                                                                                                                                                                                        | **AI-generated contribution**                                                                                                                                             | **Decision**                               | **Verification / evidence**                                                                                                                                                                                                    |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| _"Implement the Patient class from the approved SmartCare UML using type hints and basic validation. Do not add database logic."_                                                                                                                        | Generated a Patient class containing patient_id, name, dob, phone, email, and optional medical_notes, with validate() and register() methods.                             | Accepted with minor modification           | Created a valid Patient object successfully. Tested blank name, blank phone, invalid email, and future date of birth; each invalid case raised the expected error.                                                             |
| _"Implement the Practitioner class with identifier, name, and specialty. Do not add database logic."_                                                                                                                                                    | Generated a simple Practitioner class with validation for practitioner ID, name, and specialty.                                                                           | Accepted                                   | Created a valid Practitioner object. Tested empty ID, name, and specialty; invalid values were rejected. No database or scheduling service was added.                                                                          |
| _"Implement only the Appointment class from the approved SmartCare UML. Use type hints and an AppointmentStatus enum. Cancelled appointments remain as objects. Do not add database, UI, notification, or service classes. Protect status transitions."_ | Generated the Appointment class, AppointmentStatus enum, fixed 30-minute duration, overlap checking, confirmation, completion, cancellation, and rescheduling operations. | Accepted with modifications                | Compared the generated code with the approved UML. Confirmed that only Appointment-related code was included and that unsupported service classes were absent.                                                                 |
| _"Protect appointment status transitions and prevent invalid lifecycle changes."_                                                                                                                                                                        | Added methods such as confirm(), complete(), and cancel() instead of allowing unrestricted status assignment.                                                             | Accepted                                   | Tested valid transitions: Pending → Confirmed, Confirmed → Completed, and Confirmed → Cancelled. Tested invalid transitions such as Pending → Completed and repeated cancellation; errors were raised.                         |
| _"Prevent overlapping appointments for the same practitioner while allowing adjacent slots."_                                                                                                                                                            | Generated check_overlap() using appointment start and end times with a fixed 30-minute duration. Cancelled appointments are ignored.                                      | Accepted                                   | Tested appointments at 10:00 and 10:15 for the same practitioner; conflict was detected. Tested appointments at 10:00 and 10:30; adjacent appointments were allowed. Tested different practitioners; no conflict was reported. |
| _"Ensure cancelled appointments remain available for appointment history."_                                                                                                                                                                              | Kept the appointment object and changed its status to CANCELLED, recording the cancellation reason and timestamp instead of deleting it.                                  | Accepted                                   | After cancellation, the object still existed and retained its ID, patient ID, practitioner ID, reason, timestamp, and CANCELLED status.                                                                                        |
| _"Implement rescheduling with validation before changing the appointment time."_                                                                                                                                                                         | Added a reschedule() method that validates the new datetime, checks status, checks overlap, and changes the time only after validation succeeds.                          | Accepted with correction                   | Tested rescheduling to a free slot; it succeeded. Tested rescheduling to an overlapping slot; an error was raised and the original appointment time remained unchanged.                                                        |
| _"Review the generated code for unsupported features and unnecessary dependencies."_                                                                                                                                                                     | The AI initially suggested or could have introduced database access, UI logic, notification handling, and service classes.                                                | Rejected                                   | These features were removed or not implemented because Stage 4 focuses on the domain layer and the approved prompt explicitly excludes them.                                                                                   |
| _"Review the code for incorrect inheritance and class relationships."_                                                                                                                                                                                   | The generated design was checked for possible inheritance from Patient or PatientRecord.                                                                                  | Rejected inheritance; accepted association | Confirmed that Appointment stores patient_id and practitioner_id. It does not inherit from either class because an appointment has a patient and practitioner; it is not a type of either.                                     |
| _"Refactor the implementation to make it simpler and design-consistent."_                                                                                                                                                                                | Suggested protected appointment state, read-only properties, validation before mutation, and removal of unnecessary dependencies.                                         | Accepted                                   | Confirmed that status is changed only through domain methods, overlap is checked before mutation, and no SQL, notification, UI, or manager classes remain.                                                                     |

# Suggested AI prompt

\- Act as a Python pair programmer. Implement only the Appointment class from the approved SmartCare UML. Use type hints and an AppointmentStatus enum. Cancelled appointments remain as objects. Do not add database, UI, notification or service classes. Protect status transitions and explain any decision not directly visible in the UML 🡺 A py. file

_\- Design decisions:_

1. **Enum for Fixed States:** AppointmentStatus uses an enum to strictly enforce the allowed UML states.
2. **Hardcoded 30-Minute Duration:** A fixed duration simplifies overlap detection without needing a separate TimeSlot class for v0.2.
3. **Protected State Changes:** Direct mutation of \_status is restricted; state transitions must go through confirm(), complete(), or cancel().
4. **Retained Cancellation Data:** Canceled appointments are kept in memory/history to preserve their reason, timestamp, and audit trail.
5. **Association over Inheritance:** Overlap checks reference patient_id and practitioner_id directly rather than inheriting from those entities.
6. **Pre-Mutation Validation:** Inputs are validated before executing state changes (e.g., during rescheduling) to prevent corrupted or invalid states on failure.

# Reflection

\- Which AI-generated part did you modify or reject? Why? How did the approved design constrain the AI?

🡺 Refinement and restraint are often the most demanding aspects of object-oriented design, particularly when resisting the temptation to over-engineer. Throughout the implementation, the initial UML diagram served as our primary architectural boundary and single source of truth, specifically designating the Appointment class as the central business entity. While automated AI code suggestions repeatedly nudged the design toward complex abstractions, such as gratuitous service layers, appointment managers, and dedicated controllers. These additions were ultimately rejected because Bound by the scope of SmartCare v0.2, this deliberate minimalism ensures the domain model stays highly cohesive, lightweight, and easily testable. Ultimately, this experience reinforces a fundamental principle of software architecture: high-quality domain design is not defined by how many structural layers can be added, but by how cleanly and accurately it encodes only the required business logic. they introduced unneeded indirection unsupported by our functional requirements.

🡺 I rejected any AI-generated features involving database access, SQL, user-interface code, notifications, manager classes, or service classes because they were not part of the approved Appointment UML or the Stage 4 scope. I also rejected inheritance from Patient, Practitioner, or PatientRecord because an appointment is associated with a patient and practitioner; it is not a subtype of either class.

🡺 The approved design constrained the AI by limiting the implementation to the Appointment class and its agreed AppointmentStatus enum. It also required cancelled appointments to remain as objects, prevented overlapping appointments, and required protected status transitions. These constraints stopped the AI from adding unsupported features and kept the final implementation simple, focused, testable, and consistent with the SmartCare domain model.