from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


class AppointmentStatus(Enum):
    """Valid appointment lifecycle states."""

    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Appointment:
    """Represents a SmartCare clinic appointment."""

    DURATION_MINUTES: int = 30

    def __init__(
        self,
        appointment_id: str,
        patient_id: str,
        practitioner_id: str,
        time: datetime,
    ) -> None:
        self._appointment_id = appointment_id
        self._patient_id = patient_id
        self._practitioner_id = practitioner_id
        self._time = time
        self._status = AppointmentStatus.PENDING
        self._cancellation_reason: Optional[str] = None
        self._cancellation_timestamp: Optional[datetime] = None

        self._validate()

    @property
    def appointment_id(self) -> str:
        """Return the appointment identifier."""
        return self._appointment_id

    @property
    def patient_id(self) -> str:
        """Return the patient identifier."""
        return self._patient_id

    @property
    def practitioner_id(self) -> str:
        """Return the practitioner identifier."""
        return self._practitioner_id

    @property
    def time(self) -> datetime:
        """Return the appointment start time."""
        return self._time

    @property
    def status(self) -> AppointmentStatus:
        """Return the current appointment status."""
        return self._status

    @property
    def cancellation_reason(self) -> Optional[str]:
        """Return the cancellation reason, if available."""
        return self._cancellation_reason

    @property
    def cancellation_timestamp(self) -> Optional[datetime]:
        """Return the cancellation timestamp, if available."""
        return self._cancellation_timestamp

    @property
    def end_time(self) -> datetime:
        """Calculate the appointment end time."""
        return self._time + timedelta(minutes=self.DURATION_MINUTES)

    def _validate(self) -> None:
        """Validate the appointment's required data."""
        if not self._appointment_id.strip():
            raise ValueError("Appointment ID cannot be empty")

        if not self._patient_id.strip():
            raise ValueError("Patient ID cannot be empty")

        if not self._practitioner_id.strip():
            raise ValueError("Practitioner ID cannot be empty")

        if not isinstance(self._time, datetime):
            raise TypeError("Appointment time must be a datetime object")

    def check_overlap(
        self,
        other_appointments: list[Appointment],
    ) -> bool:
        """
        Return True if this appointment overlaps another active appointment
        for the same practitioner.

        Cancelled appointments do not block the time slot.
        Adjacent appointments are permitted.
        """
        for other in other_appointments:
            if other.appointment_id == self.appointment_id:
                continue

            if other.practitioner_id != self.practitioner_id:
                continue

            if other.status == AppointmentStatus.CANCELLED:
                continue

            if (
                self.time < other.end_time
                and self.end_time > other.time
            ):
                return True

        return False

    def confirm(self) -> None:
        """Change a pending appointment to confirmed."""
        if self._status != AppointmentStatus.PENDING:
            raise ValueError(
                "Only pending appointments can be confirmed"
            )

        self._status = AppointmentStatus.CONFIRMED

    def complete(self) -> None:
        """Change a confirmed appointment to completed."""
        if self._status != AppointmentStatus.CONFIRMED:
            raise ValueError(
                "Only confirmed appointments can be completed"
            )

        self._status = AppointmentStatus.COMPLETED

    def cancel(self, reason: str) -> None:
        """
        Cancel the appointment without deleting it.

        The cancellation reason and timestamp are recorded.
        """
        if not reason or not reason.strip():
            raise ValueError("Cancellation reason cannot be empty")

        if self._status == AppointmentStatus.CANCELLED:
            raise ValueError("Appointment is already cancelled")

        if self._status == AppointmentStatus.COMPLETED:
            raise ValueError(
                "Completed appointments cannot be cancelled"
            )

        self._status = AppointmentStatus.CANCELLED
        self._cancellation_reason = reason.strip()
        self._cancellation_timestamp = datetime.now()

    def reschedule(
        self,
        new_time: datetime,
        other_appointments: Optional[list[Appointment]] = None,
    ) -> None:
        """
        Reschedule the appointment after validating the new time.

        The appointment is not changed if the new time is invalid or
        overlaps another appointment.
        """
        if not isinstance(new_time, datetime):
            raise TypeError("New time must be a datetime object")

        if self._status in (
            AppointmentStatus.CANCELLED,
            AppointmentStatus.COMPLETED,
        ):
            raise ValueError(
                "Cancelled or completed appointments cannot be rescheduled"
            )

        proposed_appointment = Appointment(
            appointment_id=self._appointment_id,
            patient_id=self._patient_id,
            practitioner_id=self._practitioner_id,
            time=new_time,
        )

        proposed_appointment._status = self._status

        if proposed_appointment.check_overlap(
            other_appointments or []
        ):
            raise ValueError(
                "The new appointment time overlaps another appointment"
            )

        self._time = new_time

    def __str__(self) -> str:
        return (
            f"Appointment("
            f"id={self._appointment_id}, "
            f"patient={self._patient_id}, "
            f"practitioner={self._practitioner_id}, "
            f"time={self._time}, "
            f"status={self._status.value}"
            f")"
        )