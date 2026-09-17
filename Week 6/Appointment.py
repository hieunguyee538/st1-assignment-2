# Appointment.py
from datetime import datetime, date
from enum import Enum
from typing import Optional


class AppointmentStatus(Enum):
    """Appointment status enumeration."""
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Appointment:
    """Appointment entity managing bookings, status, and history."""

    DURATION_MINUTES = 30  # Fixed 30-minute appointments for v0.2

    def __init__(self, appointment_id: str, patient_id: str,
                 practitioner_id: str, time: datetime):
        self.appointment_id = appointment_id
        self.patient_id = patient_id  # Foreign key to Patient
        self.practitioner_id = practitioner_id  # Foreign key to Practitioner
        self.time = time
        self.status = AppointmentStatus.PENDING
        self.duration_minutes = self.DURATION_MINUTES
        self.created_timestamp = datetime.now()
        self.cancellation_reason = None  # Populated when cancelled
        self.cancellation_timestamp = None  # Populated when cancelled
        self.history_id = None  # Foreign key to AppointmentHistory

    def create(self) -> bool:
        """Create new appointment with conflict checking. Return True if successful."""
        pass

    def check_overlap(self, practitioner_id: str, time: datetime) -> bool:
        """Prevent overlapping appointments for same practitioner. Return True if overlap found."""
        pass

    def change_status(self, new_status: AppointmentStatus) -> None:
        """Transition appointment status. Record timestamp of status change."""
        pass

    def confirm(self) -> None:
        """Transition status from Pending to Confirmed."""
        pass

    def cancel(self, reason: str) -> None:
        """Cancel appointment. Store cancellation reason and timestamp."""
        pass

    def reschedule(self, new_time: datetime) -> bool:
        """Move appointment to new time. Validate new slot available. Return True if successful."""
        pass

    def get_history(self) -> 'AppointmentHistory':
        """Return immutable history of all changes to this appointment."""
        pass

    def is_cancellable(self) -> bool:
        """Check if appointment can be cancelled (not already cancelled or completed)."""
        pass