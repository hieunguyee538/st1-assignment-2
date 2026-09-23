SmartCare v0.4 - Domain Implementation Workbook

Week 7 student resource

# 1\. UML-to-Code Trace

| **UML element**                | **Python element** | **Implemented?** | **Notes**                                             |
| ------------------------------ | ------------------ | ---------------- | ----------------------------------------------------- |
| _Patient_                      | Patient class      | Yes              | Dataclass with validation.                            |
| _Patient.patient_id_           | patient_id         | Yes              | Required identifier.                                  |
| _Patient.name_                 | name               | Yes              | Required and validated.                               |
| _Patient.dob_                  | dob                | Yes              | Must be a date and cannot be in the future.           |
| _Patient.phone_                | phone              | Yes              | Required non-empty value.                             |
| _Patient.email_                | email              | Yes              | Basic format validation included.                     |
| _Patient.medical_notes_        | medical_notes      | Yes              | Optional field.                                       |
| _Practitioner_                 | Practitioner class | Yes              | Dataclass with validation.                            |
| _Practitioner.practitioner_id_ | practitioner_id    | Yes              | Required identifier.                                  |
| _Practitioner.name_            | name               | Yes              | Required and validated.                               |
| _Practitioner.specialty_       | specialty          | Yes              | Required and validated.                               |
| _Appointment_                  | Appointment class  | Yes              | Protected state and domain methods.                   |
| _Appointment_id_               | \_appointment_id   | Yes              | Exposed through read-only property.                   |
| _check_overlap()_              | check_overlap()    | Yes              | Checks active appointments for conflicts.             |
| _confirm()_                    | confirm()          | Yes              | Allows only Pending<br><br>→ Confirmed.               |
| _complete()_                   | complete()         | Yes              | Allows only Confirmed<br><br>→ Completed.             |
| _cancel()_                     | cancel()           | Yes              | Preserves the object and records cancellation data.   |
| _reschedule()_                 | reschedule()       | Yes              | Validates conflicts before changing time.             |
| _Database_                     | Repository         | No               | Deliberately excluded from the domain implementation. |
| _Notification service_         | None               | No               | Out of scope for v0.2.                                |
| _UI_                           | None               | No               | Application-layer responsibility.                     |

# 2\. Domain Invariants

| **Class**      | **Invariant / rule**                                           | **How protected**                           |
| -------------- | -------------------------------------------------------------- | ------------------------------------------- |
| _Patient_      | Patient ID cannot be blank.                                    | Patient.validate()                          |
| _Patient_      | Patient name cannot be blank.                                  | Patient.validate()                          |
| _Patient_      | DOB cannot be in the future.                                   | Patient.validate()                          |
| _Patient_      | Phone cannot be blank.                                         | Patient.validate()                          |
| _Patient_      | Email cannot be blank and must contain basic email structure.  | Patient.validate()                          |
| _Practitioner_ | Practitioner ID cannot be blank.                               | Practitioner.validate()                     |
| _Practitioner_ | Practitioner name cannot be blank.                             | Practitioner.validate()                     |
| _Practitioner_ | Specialty cannot be blank.                                     | Practitioner.validate()                     |
| _Appointment_  | Appointment ID cannot be blank.                                | Appointment.validate()                      |
| _Appointment_  | Patient and practitioner IDs are required.                     | Appointment.validate()                      |
| _Appointment_  | Appointment time must be a datetime.                           | Appointment.validate()                      |
| _Appointment_  | Only enum values may be used as status values.                 | AppointmentStatus                           |
| _Appointment_  | Same practitioner cannot have overlapping active appointments. | check_overlap()                             |
| _Appointment_  | Adjacent appointments are allowed.                             | Time-range comparison                       |
| _Appointment_  | Cancelled appointments remain as objects.                      | cancel() changes status instead of deleting |

# 3\. Composition / Inheritance Decisions

| **Relationship**           | **Decision**                      | **Rationale**                                                                         |
| -------------------------- | --------------------------------- | ------------------------------------------------------------------------------------- |
| _Patient–Appointment_      | Association, one-to-many          | A patient can have multiple appointments. An appointment refers to one patient.       |
| _Practitioner–Appointment_ | Association, one-to-many          | A practitioner can have many appointments. An appointment refers to one practitioner. |
| _Appointment–Patient_      | Not inheritance                   | An appointment is not a type of patient.                                              |
| _Appointment–Practitioner_ | Not inheritance                   | An appointment is not a type of practitioner.                                         |
| _Doctor–Practitioner_      | Possible inheritance              | Doctor may be a specialised practitioner if it has distinct behaviour.                |
| _Clinic–Appointment_       | Association/composition in future | A clinic may contain appointments, but the Clinic class is outside v0.2 scope.        |
| _AppointmentStatus_        | Enum                              | Status values are fixed states, not independent domain entities.                      |
| _CancellationReason_       | Attribute or enum                 | Cancellation reasons are simple values stored on Appointment.                         |

# 4\. AI Pair-Programming Record

| **AI contribution**                            | **Confirms?** | **Decision** | **Reason**                                          | **Verification**                                  |
| ---------------------------------------------- | ------------- | ------------ | --------------------------------------------------- | ------------------------------------------------- |
| _Use type hints_                               | Yes           | Accept ✔     | Improves readability and identifies expected types. | Signatures reviewed.                              |
| _Use AppointmentStatus enum_                   | Yes           | Accept ✔     | Matches the approved status model.                  | All four statuses tested.                         |
| _Use dataclasses for Patient and Practitioner_ | Yes           | Accept ✔     | Appropriate for small data-focused entities.        | Valid objects created successfully.               |
| _Add Patient validation_                       | Yes           | Accept ✔     | Protects patient invariants.                        | Empty name and future DOB tests failed correctly. |
| _Add Practitioner validation_                  | Yes           | Accept ✔     | Prevents incomplete practitioner objects.           | Blank specialty test failed correctly.            |
| _Add overlap detection_                        | Yes           | Accept ✔     | Directly supports duplicate-booking prevention.     | Overlapping and adjacent times tested.            |
| _Protect status transitions_                   | Yes           | Accept ✔     | Prevents invalid lifecycle changes.                 | Illegal transitions raised errors.                |
| _Use private/protected Appointment state_      | Yes           | Accept ✔     | Prevents unrestricted public mutation.              | Read-only properties expose state.                |
| _Add SQL to Appointment_                       | No            | Reject X     | Persistence does not belong in the domain entity.   | No SQL was added.                                 |
| _Add NotificationManager_                      | No            | Reject X     | Notifications are outside v0.2 scope.               | No notification dependency exists.                |
| _Inherit Appointment from PatientRecord_       | No            | Reject X     | Incorrect "is-a" relationship.                      | Appointment uses patient_id association instead.  |
| _Add PatientManager_                           | No            | Reject X     | Unnecessary indirection for this scope.             | No manager class was created.                     |
| _Delete cancelled appointments_                | No            | Reject X     | Conflicts with history and audit requirements.      | Cancelled objects remain in memory.               |

# 5\. Updated UML

\- Insert updated UML only if implementation revealed a justified design change. Explain every change.

🡺 A separate image is uploaded.