SmartCare v0.2 - Requirements Specification Template

# 1\. Problem and Scope

\- SmartCare Community Clinic manages patients and appointments with fragmented spreadsheets and paper records, which results in duplicate bookings, difficulty finding patient information, inconsistent appointment status, limited practitioner visibility, manual cancelations, unreliable appointment history, and the inability to generate operational reports.

\- Out of scope (provisional): Clinical medical records, insurance and billing, SMS notifications, patient self-service portal, multi-location support, and external system connectivity.

# 2\. Stakeholders

| **Stakeholder**        | **Need**                                                      | **Evidence**                                                |
| ---------------------- | ------------------------------------------------------------- | ----------------------------------------------------------- |
| _Clinic Receptionist_  | Quick appointment booking, patient lookup, prevent duplicates | Case study: duplicate bookings and record retrieval issues  |
| _General Practitioner_ | View daily schedule, manage availability, patient info access | Case study: limited visibility of practitioner availability |
| _Clinic Manager_       | Generate reports, track utilization, monitor efficiency       | Case study: difficulty producing operational reports        |
| _Patients_             | Appointment confirmations, view details, easy cancellation    | Implicit: need appointment tracking and management          |
| _Clinic IT Staff_      | Maintainable code, clear documentation, add features easily   | Client requirement: "small, maintainable system"            |

# 3\. Functional Requirements

FR-01: Patient Registration

FR-02: Patient Search & Retrieval

FR-03: Appointment Booking

FR-04: Duplicate Booking Prevention

FR-05: Appointment Status Management

FR-06: Practitioner Availability Calendar

FR-07: Appointment Cancellation

FR-08: Appointment Rescheduling

FR-09: Appointment History

FR-10: Operational Reporting

FR-11: Data Validation and FR-12: Role-Based Access Control

# 4\. Non-Functional Requirements

NFR-01: Reliability (99% uptime during clinic hours, 2-hour backups)

NFR-02: Usability (<2 minutes to book appointment)

NFR-03: Data Integrity (locking to prevent concurrent conflicts)

NFR-04: Maintainability (PEP 8, docstrings, modular design)

NFR-05: Performance (2-3 second response times regardless of database size)

NFR-06: Security (authentication, audit logging)

# 5\. User Stories

US-01: As a receptionist, I want to plan appointments for patients, so that I can avoid disputes with paper records.

US-02: As a receptionist, I want to cancel appointments, so I can save up time for patients who need to reschedule.

US-03: As a general practitioner, I want see my daily appointment schedule, so that I can prepare for consultations.

US-04: As a clinic manager, I want to analyze appointment data and reports, so that I can track operational efficiency.

US-05: As a receptionist, I want to searches for existing patients, so that I can avoid creating duplicate patient records.

# 6\. Acceptance Criteria

- 24 acceptance criteria (3-4 per story) in a Given-When-Then format:
- Each story includes at least one negative/failure situation and the requirements are testable and measurable.

\- Examples:

**GIVEN** that a patient exists in the system.  
**WHEN** I searched for the patient.  
**THEN** the system displays matching results with patient names and IDs. _(User 1)_

**GIVEN** I've entered a cancelation reason.  
**WHEN** I confirm the cancelation.  
**THEN** the appointment status switches to "Cancelled" and the time slot becomes available for the future. _(User 2)_

**GIVEN** there are no appointments scheduled for today.  
**WHEN** I view my schedule.  
**THEN** the system displays the message "No appointments scheduled for today". _(User 3)_

**GIVEN** I request a report.  
**WHEN** the report is generating.  
**THEN** the system displays the complete report within 5 seconds regardless of data volume. _(User 4)_

**GIVEN** no patients match my search.  
**WHEN** I perform a search with no results.  
**THEN** the system displays "No patients found" and offers option to create a new patient record. _(User 5)_

# 7\. Assumptions and Open Questions

**\- Assumptions Made:**

1. **Single Practitioner per Appointment** - Each appointment involves one patient and one practitioner only (no group consultations or multi-practitioner appointments)
2. **Advance Booking Only** - Appointments must be booked in advance; same-day booking is not supported in v0.2
3. **Standard Operating Hours** - Clinic operates Monday-Friday, 8 AM - 6 PM; appointments cannot be scheduled outside these hours
4. **All Appointments Same Duration** - All appointment types have a standard 30-minute duration (unless practitioner-specific durations are defined)
5. **Staff Computer Literacy** - All clinic staff (receptionists, practitioners, managers) have basic computer literacy and can navigate a simple web/desktop interface
6. **No Data Migration Required** - v0.2 starts with a fresh database; historical data from spreadsheets will not be imported automatically
7. **English-Only Interface** - System will be displayed in English only; multilingual support is not required for v0.2

**\- Open Questions Requiring Client Validation:**

1. **What is the maximum appointment booking window?** Can patients book 4 weeks in advance, 3 months, 6 months, or 1 year ahead?
2. **Do appointment durations vary by practitioner or service type?** Are all appointments 30 minutes, or do some practitioners require 15/45/60 minutes?
3. **Should the system notify patients of appointments?** Will v0.2 include SMS/email reminders, or is this a future enhancement?
4. **Can patients self-book appointments online?** Or can only reception staff create bookings through the system?
5. **What is the data retention policy?** How many years of historical appointment data should be kept in the system?
6. **Are there practitioner-specific constraints?** Do some practitioners have lunch breaks, blocked time for admin work, or days off that should be marked?
7. **How should no-shows be handled?** Should the system differentiate between patient cancellations and no-shows?
8. **Who can access the "Cancel Appointment" feature?** Can only receptionists cancel, or can practitioners self-cancel their appointments?

# 8\. AI Requirements Review Record

| **AI suggestion**                                                           | **Evidence?**                                                                                                               | **Decision** | **Reason**                                                                                                                                             | **Verification**                                                                                                            |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Appointment duration should be specified per practitioner, not standardized | No direct evidence in client brief, but FR-04 (Duplicate Booking Prevention) implies duration is needed to detect conflicts | Modified     | Assumption added to "Open Questions" - client must confirm if all appointments are 30 min or vary by practitioner                                      | Ask client: "Do all appointments last 30 minutes or do durations vary?"                                                     |
| Patient notification (SMS/email) should be included in v0.2                 | Not in client brief; client emphasized "simple system"                                                                      | Rejected     | Out of scope - complicates v0.2. Marked as provisional for future version                                                                              | Client brief stated "simple" and "maintainable" system; notifications add complexity                                        |
| Acceptance criteria should include negative scenarios                       | Best practice in test-driven development                                                                                    | Accepted     | All 4+ acceptance criteria per user story now include at least one failure/error case (e.g., "time slot unavailable", "appointment already cancelled") | All acceptance criteria reviewed for negative test cases ✓                                                                  |
| NFR-04 (Performance) should specify "regardless of database size"           | Ambiguous - doesn't state whether 3-second response applies to 100 appointments or 100,000                                  | Accepted     | Updated to clarify: "within 2-3 seconds regardless of database size"                                                                                   | Clearer wording prevents performance surprise during testing                                                                |
| FR-12 (Role-Based Access Control) needs specific roles defined              | Vague - doesn't list which roles can perform which actions                                                                  | Modified     | Added to assumptions: Receptionist (booking/cancellation), Practitioner (view schedule), Manager (view reports only)                                   | Roles defined in acceptance criteria - receptionist logs in to book, manager to view reports, practitioner to view schedule |