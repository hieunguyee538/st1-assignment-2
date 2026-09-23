from __future__ import annotations
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


class AppointmentStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Appointment:
    """
    Represents a clinic appointment.

    Rules enforced:
    - Appointment must contain patient_id and practitioner_id
    - Appointment duration is fixed at 30 minutes for v0.2
    - Prevent overlapping appointments for same practitioner
    - Allow only valid status transitions
    - Cancellation must record reason and timestamp
    - Cancelled appointments remain objects and are not deleted
    """

    DURATION_MINUTES: int = 30

    def __init__(
        self,
        appointment_id: str,
        patient_id: str,
        practitioner_id: str,
        time: datetime,
        status: AppointmentStatus = AppointmentStatus.PENDING,
    ) -> None:
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.practitioner_id = practitioner_id
        self.time = time
        self.status = status
        self.cancellation_reason: Optional[str] = None
        self.cancellation_timestamp: Optional[datetime] = None

    @property
    def end_time(self) -> datetime:
        return self.time + timedelta(minutes=self.DURATION_MINUTES)

    def validate(self) -> None:
        if not self.patient_id or not self.patient_id.strip():
            raise ValueError("Patient ID cannot be empty")
        if not self.practitioner_id or not self.practitioner_id.strip():
            raise ValueError("Practitioner ID cannot be empty")
        if not isinstance(self.time, datetime):
            raise TypeError("Appointment time must be a datetime object")
        if self.status not in AppointmentStatus:
            raise ValueError("Invalid appointment status")

    def check_overlap(
        self,
        other_appointments: list["Appointment"],
    ) -> bool:
        """
        Return True if this appointment overlaps with any appointment in
        other_appointments for the same practitioner.

        A conflict occurs when the time ranges intersect.
        """
        for other in other_appointments:
            if other.practitioner_id != self.practitioner_id:
                continue

            if other.appointment_id == self.appointment_id:
                continue

            if other.status == AppointmentStatus.CANCELLED:
                continue

            if self.time < other.end_time and self.end_time > other.time:
                return True

        return False

    def confirm(self) -> None:
        if self.status == AppointmentStatus.CANCELLED:
            raise ValueError("Cannot confirm a cancelled appointment")
        if self.status == AppointmentStatus.COMPLETED:
            raise ValueError("Cannot confirm a completed appointment")
        self.status = AppointmentStatus.CONFIRMED

    def complete(self) -> None:
        if self.status == AppointmentStatus.CANCELLED:
            raise ValueError("Cannot complete a cancelled appointment")
        if self.status == AppointmentStatus.PENDING:
            raise ValueError("Appointment must be confirmed before completion")
        self.status = AppointmentStatus.COMPLETED

    def cancel(self, reason: str) -> None:
        if not reason or not reason.strip():
            raise ValueError("Cancellation reason cannot be empty")
        if self.status == AppointmentStatus.CANCELLED:
            raise ValueError("This appointment is already cancelled")
        self.status = AppointmentStatus.CANCELLED
        self.cancellation_reason = reason.strip()
        self.cancellation_timestamp = datetime.now()

    def reschedule(self, new_time: datetime) -> None:
        if not isinstance(new_time, datetime):
            raise TypeError("New appointment time must be a datetime object")
        if self.status == AppointmentStatus.CANCELLED:
            raise ValueError("Cannot reschedule a cancelled appointment")
        if self.status == AppointmentStatus.COMPLETED:
            raise ValueError("Cannot reschedule a completed appointment")

        old_time = self.time
        self.time = new_time

        if self.time < old_time:
            # This is optional but protects odd invalid backdating logic
            raise ValueError("New appointment time cannot be earlier than the current time")

    def __str__(self) -> str:
        return (
            f"Appointment(id={self.appointment_id}, patient={self.patient_id}, "
            f"practitioner={self.practitioner_id}, time={self.time}, "
            f"status={self.status.value})"
        )

# Valid creation
a1 = Appointment(
    appointment_id="A1",
    patient_id="P100",
    practitioner_id="D1",
    time=datetime(2026, 9, 20, 10, 0),
)
a1.validate()
print(a1)

# Valid confirmation
a1.confirm()
print(a1.status)

# Overlap detection
a2 = Appointment(
    appointment_id="A2",
    patient_id="P101",
    practitioner_id="D1",
    time=datetime(2026, 9, 20, 10, 15),
)
print(a1.check_overlap([a2]))  # True

# Cancellation
a1.cancel("Patient request")
print(a1.status)
print(a1.cancellation_reason)

# Reschedule valid
a3 = Appointment(
    appointment_id="A3",
    patient_id="P102",
    practitioner_id="D2",
    time=datetime(2026, 9, 21, 9, 0),
)
a3.confirm()
a3.reschedule(datetime(2026, 9, 21, 9, 30))
print(a3.time)

# Invalid transitions
try:
    a1.complete()
except ValueError as e:
    print(f"Error: {e}")