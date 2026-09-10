Assignment 2 Case Study

Stage 2 Tutorial From Problems to Requirements

Week 5 | 60 minutes

# Learning goals

- Analyze stakeholders.
- Distinguish functional and non-functional requirements.
- Recognize ambiguity and unsupported requirements.
- Define scope.
- Develop user stories and acceptance criteria.
- Critique AI-generated requirements.

# Activity 1 - Stakeholder Map

| **Stakeholder**        | **Need**                                                 | **Potential conflict**                                                        |
| ---------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------- |
| _Clinic Receptionist_  | Quick easy booking, prevent duplicates, patient access   | Conflicts with Manager's detailed reporting needs (extra fields slow booking) |
| _General Practitioner_ | View own schedule, block admin time, privacy             | Conflicts with Manager's utilization visibility demands                       |
| _Clinic Manager_       | Comprehensive reporting, utilization tracking, analytics | Conflicts with Receptionist speed and GP privacy concerns                     |
| _Patients_             | Confirmations, reminders, easy cancellation              | Conflicts with Security (sharing data with external SMS services)             |
| _Clinic IT Staff_      | Simple maintainable code, clear documentation            | Conflicts with Manager's demands for rapid feature additions                  |

# Activity 2 - Functional or Non-Functional?

☑ Functional □ Non-functional The system shall allow staff to cancel an appointment.

□ Functional ☑ Non-functional The system should remain responsive for the course-scale dataset.

☑ Functional □ Non-functional The system shall retain cancelled appointments.

□ Functional ☑ Non-functional Core business logic should be independently testable.

☑ Functional □ Non-functional The system shall search for a patient by ID.

# Activity 3 - Repair Ambiguous Requirements

The system should be easy to use.

Problem: Subjective and unmeasurable.

🡺 Clarification question: How is "easy" measured? Time? Clicks? Satisfaction rate?

Patient search should be fast.

Problem: Relative term; undefined threshold.

🡺 Clarification question: What response time? For how many patients?

The system should securely manage data.

Problem: "Securely" is vague; many interpretations.

🡺 Clarification question: Encryption? Access control? Logging? Backups?

Appointments should normally be easy to cancel.

Problem: "Normally" and "easy" undefined.

🡺 Clarification question: Which appointments cancellable? How many steps? Time limit?

# Activity 4 - AI Requirements Audit

Classify each suggestion: Confirmed / Assumption requiring validation / Unsupported / Out of scope.

| **AI suggestion**                          | **Classification** | **Evidence / reason**                                                                        |
| ------------------------------------------ | ------------------ | -------------------------------------------------------------------------------------------- |
| _Patients receive SMS reminders_           | OUT OF SCOPE       | Not in client brief; adds complexity/cost; requires GDPR compliance. Future v0.3.            |
| _Facial recognition login_                 | UNSUPPORTED        | Over-engineered for small clinic; no stakeholder needs; cost/complexity unjustified. Reject. |
| _Receptionists create appointments_        | CONFIRMED          | Evidence: case study, FR-03, US-01. Core to solving duplicate booking problem.               |
| _Online payment_                           | OUT OF SCOPE       | Not in brief; marked as provisional future feature. Defer to v0.3+.                          |
| _Practitioners view schedules_             | CONFIRMED          | Evidence: case study ("limited visibility"), FR-06, US-03. Core requirement.                 |
| _AI recommends treatments_                 | UNSUPPORTED        | Medical advice requires clinician oversight; liability risks. Out of scope entirely.         |
| _Cancelled appointments remain in history_ | CONFIRMED          | Evidence: case study, FR-09, AC 4.3. Critical for audit trail.                               |

# Exit question

Why is 'AI suggested it' not sufficient evidence for a requirement?

**\- Here are some notable reasons why we should not use the phrase as evidence for a criterion:**

1. _No Stakeholder Evidence_ - AI suggestions are based on broad best practices; not actual client demands.
2. _Accepting all AI proposals_ would over-engineer the system, while the client wants a "simple, maintainable" one.
3. _AI Can Hallucinate!_ - AI may offer mismatched or impracticable features without comprehending the clinic context.
4. _Traceability & Responsibility_ - Good requirements must be traced down from stakeholder to need, requirement, and test.
5. _Verification Failure_ - If a feature fails and the sole rationale is "AI said so," you cannot justify it to the client.
6. _Violates RE Principles:_ Valid requirement = evidence + specification + testability + traceability. ≠ "AI suggested it"