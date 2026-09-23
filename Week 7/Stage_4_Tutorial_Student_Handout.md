Assignment 2 – Case Study

Stage 4 Tutorial Activities

Object-Oriented Design Decisions

Week 7 | 60 minutes

# Activity 1 - Encapsulation Review

| **Class**      | **Protected state / invariant**                                                                                                                                                                                                                                           | **Public operations**                                                      |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| _Patient_      | Patient ID, name, phone, email, and DOB must be valid. The name and contact fields cannot be blank. DOB cannot be in the future.                                                                                                                                          | validate(), register()                                                     |
| _Practitioner_ | Practitioner ID, name, and specialty cannot be blank.                                                                                                                                                                                                                     | validate()                                                                 |
| _Appointment_  | Appointment IDs and references must be present. Time must be a datetime. Status must be valid. Only legal lifecycle transitions are allowed. Active appointments for the same practitioner cannot overlap. Cancelled appointments must retain their reason and timestamp. | validate(), check_overlap(), confirm(), complete(), cancel(), reschedule() |

# Activity 2 - Composition or Inheritance?

_+) Appointment and Patient --> ✔ Composition/association □ Inheritance_

🡺 Reason: An appointment has one patient, and one patient can have many appointments. An appointment is not a type of patient. The relationship is represented by patient_id.

_+) Appointment and Practitioner --> ✔ Composition/association □ Inheritance_

🡺 Reason: An appointment is assigned to one practitioner, and one practitioner can have many appointments. An appointment is not a type of practitioner. The relationship is represented by practitioner_id.

_+) Doctor and Practitioner (hypothetical) --> □ Composition/association ✔ Inheritance_

🡺 Reason: An appointment is assigned to one practitioner, and one practitioner can have many appointments. An appointment is not a type of practitioner (only be used if a Doctor has different attributes or behaviour).

_+) Clinic and Appointment --> ✔ Composition/association □ Inheritance_

🡺 Reason: A clinic manages or contains many appointments, but an appointment is not a type of clinic (not in v0.2).

# Activity 3 - Responsibility Allocation

**\- Who decides whether SCHEDULED can become CANCELLED?**

🡺 The Appointment class decides. Cancellation is a domain rule, so it must be enforced by the domain object rather than only by the UI.

🡺 The cancel() method checks:

1. whether the reason is present
2. whether the appointment is already cancelled
3. whether the appointment is completed
4. whether cancellation data should be recorded

🡺 The UI can show a Cancel button, but it should not be responsible for deciding whether cancellation is legal.

**\- Who validates a patient name?**

🡺 The Patient class validates its own name. The UI may provide early validation for convenience, but domain-level validation is still required.

🡺 The object that owns the data should protect its own invariant.

**\- Should Appointment execute SQL? Why?**

**🡺** No, as the Appointment class should contain appointment business rules, including:

- status transitions
- cancellation rules
- rescheduling rules
- overlap detection

**🡺 It should not contain SQL because SQL is a persistence concern.**

🡺 A more suitable design: User Interface --> Application Layer --> Domain Layer --> Appointment

Database <-- Repository Layer ↓

**\- Should the UI decide whether a status transition is legal?**

**🡺** No, as the UI can: +) display available buttons _<== The UI should not own the business rule._

+) collect the cancellation reason

+) display error messages

# Activity 4 - AI Code Critique

\- AI generates an Appointment class with public status mutation, SQL inside cancel(), a NotificationManager dependency and inheritance from PatientRecord. Identify at least five design problems and corrections.

| **Design problem**                     | **Correction**                                            |
| -------------------------------------- | --------------------------------------------------------- |
| _Public status mutation_               | Use controlled lifecycle methods                          |
| _SQL inside cancel()_                  | Move persistence to a repository                          |
| _Notification dependency_              | Remove from v0.2 domain class                             |
| _Inheritance from PatientRecord_       | Use association through patient_id                        |
| _Invalid status transitions_           | Enforce legal transitions                                 |
| _Too many responsibilities_            | Separate domain, UI, persistence, security, and reporting |
| _Notification mixed with cancellation_ | Handle notification outside Appointment                   |
| _Broad error swallowing_               | Use specific exceptions                                   |
| _State mutated before validation_      | Validate first, mutate second                             |

# Exit question

\- Why can code be object-oriented (OO) syntactically but still have poor object-oriented design?

\- Syntactically using classes, methods, constructors, and inheritance does not inherently yield good object-oriented design. True OO quality relies on proper responsibility assignment, and strong encapsulation.

+) Consider an Appointment class. It can feature all the standard syntax, yet still reflect poor design if it:

- Exposes status attributes to unrestricted public mutation.
- Executes database queries directly.
- Handles notification delivery.
- Controls presentation and UI logic.
- Validates unrelated patient properties.
- Inappropriately inherits from PatientRecord.

🡺 Mixing these concerns produces tight coupling, weak encapsulation, skewed domain relationships, and bloated classes that violate the Single Responsibility Principle.

\- In the SmartCare architecture, responsibilities are cleanly separated:

- **Appointment** exclusively governs appointment-specific domain rules, including state transitions, cancellation, rescheduling, and schedule conflict/overlap checks.
- **Patient** owns its own data validation.
- **Database Access** is isolated within a dedicated repository.
- **User Interaction** resides in the UI or application layer.
- **Domain Relationships** reflect reality: Appointment links to Patient through an association ("has-a"), completely avoiding incorrect IS-A inheritance hierarchies.