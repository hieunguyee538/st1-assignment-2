#from domain.models import Appointment
from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, Sequence

class AppointmentRepository(ABC):
    @abstractmethod
    def save(self, appointment: Appointment) -> None:
        """Persists a new or modified appointment aggregate."""
        pass

    @abstractmethod
    def find_by_id(self, appointment_id: str) -> Optional[Appointment]:
        """Retrieves a single appointment by its identifier."""
        pass

    @abstractmethod
    def find_by_practitioner_and_date(
        self, practitioner_id: str, appointment_date: date
    ) -> Sequence[Appointment]:
        """Retrieves appointments required for slot availability and booking logic."""
        pass

    @abstractmethod
    def find_by_patient(self, patient_id: str) -> List:
        pass