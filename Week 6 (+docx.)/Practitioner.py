# Practitioner.py
from datetime import datetime, date
from typing import Dict, List, Tuple, Optional


class Practitioner:
    """Practitioner entity managing availability and scheduling."""

    CLINIC_START_HOUR = 8  # 8 AM
    CLINIC_END_HOUR = 18  # 6 PM

    def __init__(self, practitioner_id: str, user_id: str, name: str, specialty: str):
        self.practitioner_id = practitioner_id
        self.user_id = user_id  # Foreign key to User (for authentication)
        self.name = name
        self.specialty = specialty
        self.working_hours = {}  # {day: (start_hour, end_hour)} e.g., {"Monday": (8, 18)}
        self.blocked_time = []  # List of {"start": datetime, "end": datetime, "reason": str}
        self.appointments = []  # List of appointment IDs

    def get_available_slots(self, date_range: Tuple[date, date]) -> list:
        """Return available time slots for next 4 weeks. Return list of free datetime slots."""
        pass

    def get_booked_slots(self, date_obj: date) -> list:
        """Get all booked appointment times for a specific date. Return list of Appointment objects."""
        pass

    def check_availability(self, time: datetime) -> bool:
        """Check if practitioner is available at specific time. Return True if available."""
        pass

    def add_blocked_time(self, start: datetime, end: datetime, reason: str = "") -> None:
        """Block practitioner time (lunch, admin, vacation). Store in blocked_time list."""
        pass

    def get_utilization(self, date_range: Tuple[date, date]) -> float:
        """Calculate practitioner utilization % (booked / available slots * 100) for date range."""
        pass

    def get_appointments(self) -> list:
        """Retrieve all appointments for this practitioner. Return list of Appointment objects."""
        pass